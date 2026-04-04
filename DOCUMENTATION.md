# Complete Technical Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Module Documentation](#module-documentation)
3. [API Reference](#api-reference)
4. [Database & State Management](#database--state-management)
5. [Error Handling](#error-handling)
6. [Development Guide](#development-guide)

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Application                        │
│                  (Web/Mobile/CLI)                            │
└─────────────────────────────────────────────────────────────┘
                            │
                    HTTP/REST API
                            │
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Server                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              HTTP Endpoints                          │   │
│  │  ├─ GET  /health                                    │   │
│  │  ├─ GET  /                                          │   │
│  │  ├─ POST /chat                                      │   │
│  │  ├─ POST /clear                                     │   │
│  │  └─ POST /summarize                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │      ChatbotService (app/chatbot.py)                │   │
│  │  ├─ send_message()                                  │   │
│  │  ├─ clear_conversation()                            │   │
│  │  └─ get_conversation_summary()                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                   OpenAI API (HTTP)
                            │
┌─────────────────────────────────────────────────────────────┐
│                 OpenAI Backend Services                      │
│              (GPT-3.5-turbo, GPT-4, etc.)                   │
└─────────────────────────────────────────────────────────────┘
```

### Request-Response Flow

```
Client Request
    │
    ├─ Validation (Pydantic)
    │
    ├─ ChatbotService.send_message()
    │
    ├─ Build messages list with history
    │
    ├─ Call OpenAI API
    │
    ├─ Update conversation history
    │
    └─ Return ChatResponse
```

---

## Module Documentation

### 1. `config/settings.py`

**Purpose**: Central configuration management for the application.

**Class: Settings**
```python
class Settings:
    OPENAI_API_KEY: str          # OpenAI API authentication
    OPENAI_MODEL: str            # Model name (gpt-3.5-turbo, gpt-4, etc.)
    DEBUG: bool                  # Enable debug mode
    HOST: str                    # Server hostname
    PORT: int                    # Server port
    MAX_TOKENS: int              # Maximum response tokens
    TEMPERATURE: float           # Response randomness (0-2)
    APP_NAME: str               # Application name
    APP_VERSION: str            # Version string
    
    def validate()              # Validates required settings
```

**Environment Variables**:
```
OPENAI_API_KEY          Required   OpenAI API key
OPENAI_MODEL           Optional   Model to use (default: gpt-3.5-turbo)
DEBUG                  Optional   Debug mode (default: False)
HOST                   Optional   Server host (default: 0.0.0.0)
PORT                   Optional   Server port (default: 8000)
MAX_TOKENS            Optional   Max tokens (default: 2000)
TEMPERATURE           Optional   Temperature (default: 0.7)
```

**Flow**:
1. Load environment variables from `.env`
2. Parse and validate configuration
3. Validate required fields (API key)
4. Provide global `settings` object

### 2. `app/models.py`

**Purpose**: Pydantic data validation models for API requests/responses.

**Message Model**
```python
class Message(BaseModel):
    role: str       # "user" or "assistant"
    content: str    # Message text
```

**ChatRequest Model**
```python
class ChatRequest(BaseModel):
    message: str                              # Required user message
    conversation_history: List[Message] = []  # Optional conversation history
```

**ChatResponse Model**
```python
class ChatResponse(BaseModel):
    message: str                    # Assistant response
    conversation_history: List[Message]  # Updated history
    model: str                     # Model used
    tokens_used: Optional[int]     # Tokens consumed
```

**HealthResponse Model**
```python
class HealthResponse(BaseModel):
    status: str    # "healthy"
    version: str   # Version number
    model: str     # Current model
```

### 3. `app/chatbot.py`

**Purpose**: Core chatbot service for OpenAI API interaction.

**Class: ChatbotService**

**Initialization**:
```python
def __init__(self):
    # Sets OpenAI API key
    # Loads model, max_tokens, temperature from settings
```

**Method: send_message()**
```python
def send_message(
    user_message: str,
    conversation_history: List[Dict] = None
) -> Tuple[str, List[Dict], int]:
    """
    Args:
        user_message: User's input message
        conversation_history: Previous messages (optional)
    
    Returns:
        (response_message, updated_history, tokens_used)
    """
```

**Flow**:
1. Initialize messages list with system prompt
2. Add conversation history to context
3. Append current user message
4. Call OpenAI API
5. Extract response text and token count
6. Update conversation history
7. Return results

**Error Handling**:
- `AuthenticationError`: Invalid API key
- `RateLimitError`: API rate limit exceeded
- `APIError`: General OpenAI API error

**Method: clear_conversation()**
```python
def clear_conversation() -> List[Dict]:
    # Returns empty list to reset history
```

**Method: get_conversation_summary()**
```python
def get_conversation_summary(
    conversation_history: List[Dict]
) -> str:
    # Generates a 2-3 sentence summary of conversation
```

### 4. `app/main.py`

**Purpose**: FastAPI application with API endpoints.

**Initialization**:
```python
app = FastAPI(
    title="OpenAI Chatbot API",
    version="1.0.0",
    description="..."
)

# CORS middleware for cross-origin requests
# ChatbotService instance
# Logger configuration
```

**Endpoints**:

#### GET /
Root endpoint returning welcome message and links.

#### GET /health
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model": "gpt-3.5-turbo"
}
```

#### POST /chat
Main chat endpoint.

**Request**:
```json
{
  "message": "user message",
  "conversation_history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

**Response**:
```json
{
  "message": "response text",
  "conversation_history": [...],
  "model": "gpt-3.5-turbo",
  "tokens_used": 45
}
```

**Error Handling**:
- Returns HTTPException with status 500 on errors
- Logs error details

#### POST /clear
Clears conversation history.

**Response**:
```json
{
  "message": "Conversation cleared",
  "history": []
}
```

#### POST /summarize
Generates conversation summary.

**Request**:
```json
{
  "conversation_history": [...]
}
```

**Response**:
```json
{
  "summary": "Summary text..."
}
```

---

## API Reference

### Base URL
```
http://localhost:8000
```

### Content-Type
All requests expect `Content-Type: application/json`

### Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (validation error) |
| 500 | Server Error (API error) |

### Request Headers
```
Content-Type: application/json
```

### Response Headers
```
Content-Type: application/json
```

### Example Request-Response Cycle

**Request**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is machine learning?",
    "conversation_history": []
  }'
```

**Response** (200 OK):
```json
{
  "message": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed...",
  "conversation_history": [
    {
      "role": "user",
      "content": "What is machine learning?"
    },
    {
      "role": "assistant",
      "content": "Machine learning is a subset of artificial intelligence..."
    }
  ],
  "model": "gpt-3.5-turbo",
  "tokens_used": 87
}
```

---

## Database & State Management

### Current Architecture
The application uses **stateless, in-memory conversation management**:

- **Conversation History**: Maintained on client side
- **Token Tracking**: Per-request basis
- **No Database**: All state is ephemeral

### Conversation State Flow

```
Client                          Server
   │                               │
   ├─ Store conversation history   │
   │  [msg1, msg2, ...]            │
   │                               │
   ├─ POST /chat                   │
   │  [msg1, msg2, ...] + new msg  │
   │                               │
   │                     Process ──┤
   │                     Call API  │
   │                     Update    │
   │                               │
   │  response + updated history ──┤
   │                               │
   ├─ Update local history         │
   │  [msg1, msg2, ..., new]       │
   │                               │
```

### Future Database Integration

For persistence, consider adding:

```python
# SQLAlchemy models example
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class ConversationMessage(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    tokens_used = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
```

---

## Error Handling

### Error Hierarchy

```
Exception
├─ openai.error.AuthenticationError
│  └─ "Invalid OpenAI API key"
│
├─ openai.error.RateLimitError
│  └─ "OpenAI API rate limit exceeded"
│
├─ openai.error.APIError
│  └─ "OpenAI API error: ..."
│
└─ ValueError
   └─ HTTPException (400)
```

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid OpenAI API key | Wrong/missing API key | Check `.env` file |
| Rate limit exceeded | Too many requests | Wait and retry |
| Max tokens exceeded | Response too long | Increase MAX_TOKENS |
| Connection error | Network issue | Check internet |

### Logging

All errors are logged at `ERROR` level:
```
ERROR - Validation error: Invalid message
ERROR - Error: Invalid OpenAI API key
```

---

## Development Guide

### Setup Development Environment

```bash
# Clone repository
cd "ChatBot Using OpenAI"

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API key
```

### Running in Development Mode

```bash
python -m uvicorn app.main:app --reload
```

**Flags**:
- `--reload`: Auto-restart on code changes
- `--log-level debug`: Show debug logs
- `--host 0.0.0.0`: Accept external connections

### Testing

Create a test file `test_chatbot.py`:

```python
import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint():
    response = client.post("/chat", json={
        "message": "Hello",
        "conversation_history": []
    })
    assert response.status_code == 200
    assert "message" in response.json()
```

Run tests:
```bash
pytest test_chatbot.py -v
```

### Code Style

Follow PEP 8:
```bash
pip install black flake8
black app/
flake8 app/
```

### Adding New Features

1. **Add to models.py** (if new request/response type)
2. **Add to chatbot.py** (if new service method)
3. **Add endpoint to main.py**
4. **Document in README.md**
5. **Test the feature**

### Extension Points

#### Adding a new endpoint
```python
@app.post("/new-endpoint", tags=["Chat"])
async def new_endpoint(request: SomeRequest):
    try:
        result = chatbot.some_method()
        return {"result": result}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

#### Adding a new service method
```python
class ChatbotService:
    def new_method(self, param1: str) -> str:
        # Implementation
        return result
```

---

## Performance Tuning

### Token Optimization
```python
# Reduce token usage
MAX_TOKENS = 500  # Shorter responses
TEMPERATURE = 0.5  # More focused
```

### Response Time
```
Average: 1-3 seconds
Network: ~500ms (OpenAI)
Processing: ~100ms
```

### Cost Estimation
- GPT-3.5-turbo: ~$0.0005 per 1K tokens
- GPT-4: ~$0.03 per 1K tokens

Track usage:
```python
total_tokens = 0
for response in responses:
    total_tokens += response.tokens_used
cost = total_tokens * 0.0005 / 1000
```

---

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Use environment-specific `.env`
- [ ] Set up proper CORS origins
- [ ] Add rate limiting
- [ ] Add request logging
- [ ] Set up error tracking (Sentry)
- [ ] Use HTTPS
- [ ] Add authentication
- [ ] Set up monitoring

### Example Production Environment
```env
DEBUG=False
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=1000
```

---

## Conclusion

This documentation provides a comprehensive overview of the chatbot application architecture, components, and usage. For updates or questions, refer to the code comments and README.md file.
