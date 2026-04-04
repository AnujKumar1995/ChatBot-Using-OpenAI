"""FastAPI application for the chatbot."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from config.settings import settings
from app.models import ChatRequest, ChatResponse, HealthResponse, Message
from app.chatbot import ChatbotService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A chatbot API powered by OpenAI"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot service
chatbot = ChatbotService()


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to OpenAI Chatbot API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        model=settings.OPENAI_MODEL
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Send a message to the chatbot and get a response.
    
    The API maintains conversation history to provide context-aware responses.
    
    **Request body:**
    - `message`: The user's message (required)
    - `conversation_history`: Previous messages in the conversation (optional)
    
    **Response:**
    - `message`: The chatbot's response
    - `conversation_history`: Updated conversation history
    - `model`: The OpenAI model used
    - `tokens_used`: Number of tokens used for this request
    """
    try:
        logger.info(f"Received message: {request.message[:50]}...")
        
        # Convert Pydantic models to dicts for chatbot service
        history = None
        if request.conversation_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ]
        
        # Get response from chatbot
        response_message, updated_history, tokens_used = chatbot.send_message(
            request.message,
            history
        )
        
        # Convert updated history back to Pydantic models
        conversation_history = [
            Message(role=msg["role"], content=msg["content"])
            for msg in updated_history
        ]
        
        logger.info(f"Response generated with {tokens_used} tokens")
        
        return ChatResponse(
            message=response_message,
            conversation_history=conversation_history,
            model=settings.OPENAI_MODEL,
            tokens_used=tokens_used
        )
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear", tags=["Chat"])
async def clear_conversation():
    """Clear the conversation history."""
    try:
        history = chatbot.clear_conversation()
        logger.info("Conversation cleared")
        return {"message": "Conversation cleared", "history": history}
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize", tags=["Chat"])
async def summarize_conversation(request: ChatRequest):
    """Get a summary of the current conversation."""
    try:
        if not request.conversation_history:
            return {"summary": "No conversation to summarize"}
        
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]
        
        summary = chatbot.get_conversation_summary(history)
        logger.info("Conversation summarized")
        return {"summary": summary}
    
    except Exception as e:
        logger.error(f"Error summarizing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
