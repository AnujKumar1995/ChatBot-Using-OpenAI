"""FastAPI application for the Customer Support Chatbot."""
import uuid
import time
from collections import defaultdict
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path
import logging
import json

from config.settings import settings
from app.models import ChatRequest, ChatResponse, HealthResponse, Message, FeedbackRequest
from app.chatbot import ChatbotService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A customer support chatbot API powered by OpenAI",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = ChatbotService()

# Simple in-memory rate limiter
_rate_limit_store: dict = defaultdict(list)


def _check_rate_limit(client_ip: str) -> bool:
    now = time.time()
    window = 60
    _rate_limit_store[client_ip] = [
        t for t in _rate_limit_store[client_ip] if now - t < window
    ]
    if len(_rate_limit_store[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        return False
    _rate_limit_store[client_ip].append(now)
    return True


# --- API Routes ---

@app.get("/api", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        model=settings.active_model,
    )


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest, req: Request):
    client_ip = req.client.host
    if not _check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please wait and try again.")

    try:
        logger.info(f"Message from {client_ip}: {request.message[:50]}...")

        history = None
        if request.conversation_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ]

        response_message, updated_history, tokens_used = await chatbot.send_message(
            request.message, history
        )

        conversation_history = [
            Message(role=msg["role"], content=msg["content"])
            for msg in updated_history
        ]

        session_id = request.session_id or str(uuid.uuid4())

        return ChatResponse(
            message=response_message,
            conversation_history=conversation_history,
            model=settings.active_model,
            tokens_used=tokens_used,
            session_id=session_id,
        )

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream", tags=["Chat"])
async def chat_stream(request: ChatRequest, req: Request):
    client_ip = req.client.host
    if not _check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    history = None
    if request.conversation_history:
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]

    async def event_generator():
        try:
            async for token in chatbot.stream_message(request.message, history):
                yield f"data: {json.dumps({'token': token})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/api/clear", tags=["Chat"])
async def clear_conversation():
    history = chatbot.clear_conversation()
    return {"message": "Conversation cleared", "history": history}


@app.post("/api/feedback", tags=["Feedback"])
async def submit_feedback(feedback: FeedbackRequest):
    logger.info(f"Feedback: session={feedback.session_id} rating={feedback.rating}")
    return {"message": "Thank you for your feedback!"}


# --- Serve React Frontend ---
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "build"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = FRONTEND_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / "index.html")



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
