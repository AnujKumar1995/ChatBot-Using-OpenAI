"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    role: MessageRole
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_history: Optional[List[Message]] = None
    session_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "How do I reset my password?",
                "conversation_history": [],
                "session_id": "abc123"
            }
        }


class ChatResponse(BaseModel):
    message: str
    conversation_history: List[Message]
    model: str
    tokens_used: Optional[int] = None
    session_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    model: str


class FeedbackRequest(BaseModel):
    session_id: str
    message_index: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
