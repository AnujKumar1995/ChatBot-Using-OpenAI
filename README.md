# Customer Support Chatbot — OpenAI + React + FastAPI

A production-ready customer support chatbot with a responsive React frontend, FastAPI backend, OpenAI integration, streaming responses, and fine-tuning support.

![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square) ![Frontend](https://img.shields.io/badge/Frontend-React%2018-61DAFB?style=flat-square) ![AI](https://img.shields.io/badge/AI-OpenAI%20GPT--4o--mini-412991?style=flat-square) ![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED?style=flat-square)

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Project Structure](#project-structure)
5. [Backend API](#backend-api)
6. [Frontend](#frontend)
7. [Fine-Tuning Your Model](#fine-tuning-your-model)
8. [Configuration](#configuration)
9. [Docker Deployment](#docker-deployment)
10. [Development](#development)
11. [Troubleshooting](#troubleshooting)

---

## Features

- **Responsive Chat UI** — Mobile-first React interface with message bubbles, typing indicators, auto-scroll
- **Customer Support Persona** — Pre-configured system prompt for professional, empathetic responses
- **Streaming Support** — Server-Sent Events (SSE) for real-time token-by-token responses
- **Conversation History** — Maintains context across messages within a session
- **Quick Action Buttons** — Common customer queries available with one click
- **Rate Limiting** — Configurable per-minute request limits
- **Fine-Tuning Pipeline** — Scripts & training data to customize the model to your business
- **Session Management** — Track conversations with unique session IDs
- **Feedback System** — Customers can rate responses
- **Docker Ready** — Multi-stage build for one-command deployment
- **API Documentation** — Auto-generated Swagger/OpenAPI docs at `/docs`

---

## Architecture

```
┌─────────────────────────────────┐
│         React Frontend          │
│  (responsive chat UI)           │
│  Port 3000 (dev) / served by    │
│  FastAPI in production          │
└──────────┬──────────────────────┘
           │ HTTP / SSE
┌──────────▼──────────────────────┐
│       FastAPI Backend           │
│  /api/chat     - send message   │
│  /api/chat/stream - SSE stream  │
│  /api/health   - health check   │
│  /api/clear    - reset session  │
│  /api/feedback - user feedback  │
│  Port 8000                      │
└──────────┬──────────────────────┘
           │ HTTPS
┌──────────▼──────────────────────┐
│       OpenAI API                │
│  gpt-4o-mini (or fine-tuned)    │
└─────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key — get one at **https://platform.openai.com/api-keys**

### 1. Clone & configure

```bash
cd "ChatBot Using OpenAI"
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Start the backend

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Start the frontend

```bash
cd frontend
npm install
npm start
# Opens http://localhost:3000
```

### 4. Or use Docker (one command)

```bash
docker-compose up --build
# Opens http://localhost:8000
```

---

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, routes, rate limiting, static file serving
│   ├── chatbot.py           # Async OpenAI service with streaming
│   └── models.py            # Pydantic request/response models
├── config/
│   └── settings.py          # Environment-based configuration
├── frontend/
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js           # Main application component
│       ├── index.js          # React entry point
│       ├── components/
│       │   ├── Header.js     # Chat header with status & clear button
│       │   ├── MessageList.js # Message display with markdown support
│       │   ├── ChatInput.js  # Auto-resizing input with send/cancel
│       │   └── QuickActions.js # Suggested question buttons
│       ├── hooks/
│       │   └── useChat.js    # Chat state management hook
│       └── styles/
│           └── index.css     # Complete responsive styles
├── training_data/
│   └── customer_support_training.jsonl  # Sample fine-tuning data
├── fine_tune.py             # Fine-tuning CLI tool
├── docker-compose.yml
├── Dockerfile               # Multi-stage build (Node + Python)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Backend API

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api` | Welcome message & version |
| `GET` | `/api/health` | Health check (status, model, version) |
| `POST` | `/api/chat` | Send message, get response |
| `POST` | `/api/chat/stream` | Send message, get SSE stream |
| `POST` | `/api/clear` | Clear conversation |
| `POST` | `/api/feedback` | Submit rating for a response |
| `GET` | `/docs` | Interactive Swagger documentation |

### Chat Request

```json
POST /api/chat
{
  "message": "How do I reset my password?",
  "conversation_history": [],
  "session_id": "optional-session-id"
}
```

### Chat Response

```json
{
  "message": "I'd be happy to help you reset your password! ...",
  "conversation_history": [
    {"role": "user", "content": "How do I reset my password?"},
    {"role": "assistant", "content": "I'd be happy to help..."}
  ],
  "model": "gpt-4o-mini",
  "tokens_used": 156,
  "session_id": "abc-123-def"
}
```

### Streaming Response (SSE)

```
POST /api/chat/stream

data: {"token": "I'd"}
data: {"token": " be"}
data: {"token": " happy"}
...
data: [DONE]
```

---

## Frontend

The React frontend provides a responsive customer support chat experience:

- **Mobile-first design** — works on phone, tablet, and desktop
- **Markdown rendering** — bot responses support formatting, lists, code blocks
- **Typing indicator** — animated dots while waiting for response
- **Auto-scroll** — messages scroll into view automatically
- **Quick actions** — pre-built question buttons for common queries
- **Cancel support** — abort in-flight requests
- **Error handling** — toast notifications for errors with auto-dismiss

### Environment Variables (Frontend)

| Variable | Default | Description |
|----------|---------|-------------|
| `REACT_APP_API_URL` | `/api` | Backend API base URL |

For development with separate frontend/backend, the `proxy` field in `package.json` forwards API requests to `http://localhost:8000`.

---

## Fine-Tuning Your Model

Fine-tuning lets you customize the chatbot's responses to match your company's tone, products, and policies.

### OpenAI Links

| Resource | URL |
|----------|-----|
| **Fine-Tuning Dashboard** | https://platform.openai.com/finetune |
| **API Keys** | https://platform.openai.com/api-keys |
| **Usage & Billing** | https://platform.openai.com/usage |
| **Fine-Tuning Guide** | https://platform.openai.com/docs/guides/fine-tuning |
| **Training Data Format** | https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset |
| **Models Overview** | https://platform.openai.com/docs/models |
| **Playground** | https://platform.openai.com/playground |

### Step-by-Step Fine-Tuning

#### 1. Prepare training data

Edit `training_data/customer_support_training.jsonl`. Each line is a JSON object:

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful customer support agent."},
    {"role": "user", "content": "How do I reset my password?"},
    {"role": "assistant", "content": "Here's how to reset your password: ..."}
  ]
}
```

**Best practices:**
- Include **50-100+ examples** for good results
- Cover all common customer scenarios
- Use your actual company's tone and policies
- Include edge cases and escalation examples
- Add multi-turn conversations for complex scenarios

#### 2. Validate your data

```bash
python fine_tune.py validate
```

#### 3. Upload & start training

```bash
python fine_tune.py train
```

Training typically takes 10-30 minutes depending on dataset size.

#### 4. Check status

```bash
python fine_tune.py status
```

#### 5. Use the fine-tuned model

Once complete, copy the model ID and add to `.env`:

```bash
OPENAI_FINE_TUNED_MODEL=ft:gpt-4o-mini-2024-07-18:your-org::abc123
```

Restart the server — it will automatically prefer the fine-tuned model.

#### Alternative: Use OpenAI Dashboard

1. Go to https://platform.openai.com/finetune
2. Click **Create** → upload your JSONL file
3. Select `gpt-4o-mini` as base model
4. Start training and wait for completion
5. Copy the model ID to your `.env`

---

## Configuration

All configuration is via environment variables (`.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Base model to use |
| `OPENAI_FINE_TUNED_MODEL` | *(empty)* | Fine-tuned model (overrides base) |
| `COMPANY_NAME` | `Our Company` | Company name in system prompt |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `MAX_TOKENS` | `2000` | Max response tokens |
| `TEMPERATURE` | `0.7` | Response creativity (0.0-2.0) |
| `RATE_LIMIT_PER_MINUTE` | `30` | Max requests per IP per minute |
| `DEBUG` | `False` | Enable debug mode |

---

## Docker Deployment

### Build & run

```bash
docker-compose up --build -d
```

### View logs

```bash
docker-compose logs -f chatbot
```

### Stop

```bash
docker-compose down
```

The Docker image uses a **multi-stage build**:
1. **Stage 1** — Builds the React frontend with Node.js
2. **Stage 2** — Runs the FastAPI server with the built frontend assets

---

## Development

### Backend only

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
# API docs at http://localhost:8000/docs
```

### Frontend only

```bash
cd frontend && npm start
# Proxies API calls to http://localhost:8000
```

### Run both (development)

Open two terminals:
```bash
# Terminal 1 - Backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend && npm start
```

### Testing with curl

```bash
# Health check
curl http://localhost:8000/api/health

# Send a message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Stream a response
curl -N -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about your return policy"}'
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `OPENAI_API_KEY is not set` | Copy `.env.example` to `.env` and add your key |
| `Rate limit exceeded` | Wait 60 seconds or increase `RATE_LIMIT_PER_MINUTE` |
| `Module not found` (backend) | Run `pip install -r requirements.txt` |
| `npm start` fails | Run `cd frontend && npm install` first |
| CORS errors in browser | Backend CORS allows all origins by default |
| Fine-tuning job failed | Run `python fine_tune.py status` for error details |
| Docker build fails | Ensure Docker Desktop is running |

---

## License

MIT
