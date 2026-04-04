"""Pydantic models for request/response validation."""
from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    """Single message in conversation."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_history: Optional[List[Message]] = None
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "message": "What is Python?",
                "conversation_history": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hello! How can I help you today?"}
                ]
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    message: str
    conversation_history: List[Message]
    model: str
    tokens_used: Optional[int] = None
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "message": "Python is a popular programming language...",
                "conversation_history": [
                    {"role": "user", "content": "What is Python?"},
                    {"role": "assistant", "content": "Python is a popular programming language..."}
                ],
                "model": "gpt-3.5-turbo",
                "tokens_used": 45
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    version: str
    model: str
