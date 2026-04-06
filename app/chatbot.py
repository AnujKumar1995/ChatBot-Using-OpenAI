"""OpenAI Customer Support Chatbot service."""
from openai import AsyncOpenAI
from typing import List, Dict, Tuple, AsyncGenerator
from config.settings import settings

CUSTOMER_SUPPORT_PROMPT = f"""You are a friendly, professional customer support agent for {settings.COMPANY_NAME}.

Your responsibilities:
- Answer customer questions clearly and helpfully
- Help troubleshoot issues step by step
- Provide information about products, services, and policies
- Escalate complex issues by advising the customer to contact a human agent
- Always maintain a polite, empathetic, and professional tone

Guidelines:
- Keep responses concise but thorough
- If you don't know something, say so honestly rather than guessing
- Ask clarifying questions when the customer's issue is unclear
- Provide step-by-step instructions when helping with technical issues
- End responses by asking if there's anything else you can help with
- Never share sensitive information or make promises you can't keep
- Use simple language, avoid jargon unless the customer uses it first"""


class ChatbotService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.active_model
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE

    async def send_message(
        self,
        user_message: str,
        conversation_history: List[Dict] = None
    ) -> Tuple[str, List[Dict], int]:
        if conversation_history is None:
            conversation_history = []

        messages = [{"role": "system", "content": CUSTOMER_SUPPORT_PROMPT}]

        for msg in conversation_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        messages.append({"role": "user", "content": user_message})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            assistant_message = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            conversation_history.append({"role": "user", "content": user_message})
            conversation_history.append({"role": "assistant", "content": assistant_message})

            return assistant_message, conversation_history, tokens_used

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def stream_message(
        self,
        user_message: str,
        conversation_history: List[Dict] = None
    ) -> AsyncGenerator[str, None]:
        if conversation_history is None:
            conversation_history = []

        messages = [{"role": "system", "content": CUSTOMER_SUPPORT_PROMPT}]
        for msg in conversation_history:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
        messages.append({"role": "user", "content": user_message})

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def clear_conversation(self) -> List[Dict]:
        return []
