"""OpenAI Chatbot service."""
import openai
import httpx
from typing import List, Dict, Tuple
from config.settings import settings


class ChatbotService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        """Initialize the chatbot service with OpenAI API key."""
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
    
    def send_message(
        self,
        user_message: str,
        conversation_history: List[Dict] = None
    ) -> Tuple[str, List[Dict], int]:
        """
        Send a message to OpenAI and get a response.
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            
        Returns:
            Tuple of (response_message, updated_history, tokens_used)
        """
        if conversation_history is None:
            conversation_history = []
        
        # Create messages list with system prompt and conversation history
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Provide clear and concise responses."
            }
        ]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract response
            assistant_message = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Update conversation history
            conversation_history.append({
                "role": "user",
                "content": user_message
            })
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message, conversation_history, tokens_used
        
        except openai.AuthenticationError:
            raise Exception("Invalid OpenAI API key")
        except openai.RateLimitError:
            raise Exception("OpenAI API rate limit exceeded. Please try again later.")
        except openai.APIError as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def clear_conversation(self) -> List[Dict]:
        """Clear conversation history."""
        return []
    
    def get_conversation_summary(self, conversation_history: List[Dict]) -> str:
        """
        Generate a summary of the conversation.
        
        Args:
            conversation_history: The conversation to summarize
            
        Returns:
            Summary text
        """
        if not conversation_history:
            return "No conversation history"
        
        messages = [
            {
                "role": "system",
                "content": "Summarize the following conversation in 2-3 sentences."
            },
            {
                "role": "user",
                "content": "Conversation:\n" + "\n".join([
                    f"{msg['role'].capitalize()}: {msg['content']}"
                    for msg in conversation_history
                ])
            }
        ]
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=200,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Could not generate summary: {str(e)}"
