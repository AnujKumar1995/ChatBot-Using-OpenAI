# Project File Structure Documentation

## Directory Tree

```
ChatBot Using OpenAI/
├── app/                           # Main application package
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # FastAPI application & endpoints
│   ├── chatbot.py                # ChatbotService class
│   └── models.py                 # Pydantic models for validation
├── config/                        # Configuration package
│   └── settings.py               # Settings & environment variables
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore file
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose setup
├── README.md                     # Main documentation
├── DOCUMENTATION.md              # Technical documentation
├── QUICKSTART.md                 # Quick start guide
├── PROJECT_STRUCTURE.md          # This file
├── test_chatbot.py              # Automated test suite
├── example_client.py            # Example client implementation
└── .env                         # Environment variables (local)
```

## File Descriptions

### Application Files

#### `app/main.py`
- **Purpose**: Main FastAPI application
- **Contains**: 
  - FastAPI app initialization
  - CORS middleware setup
  - All API endpoints
  - Error handling
  - Logging configuration
- **Key Functions**:
  - `root()` - Welcome endpoint
  - `health_check()` - Health check
  - `chat()` - Main chat endpoint
  - `clear_conversation()` - Clear history
  - `summarize_conversation()` - Generate summary

#### `app/chatbot.py`
- **Purpose**: Core chatbot service
- **Contains**: ChatbotService class
- **Key Methods**:
  - `send_message()` - Send message to OpenAI
  - `clear_conversation()` - Clear history
  - `get_conversation_summary()` - Summarize conversation
- **Responsibilities**:
  - Manage OpenAI API interactions
  - Handle conversation history
  - Error handling for API errors

#### `app/models.py`
- **Purpose**: Pydantic data models
- **Contains**:
  - `Message` - Single message model
  - `ChatRequest` - Chat request model
  - `ChatResponse` - Chat response model
  - `HealthResponse` - Health check response model
- **Responsibilities**:
  - Request/response validation
  - JSON schema generation
  - Type hints and documentation

#### `config/settings.py`
- **Purpose**: Configuration management
- **Contains**: Settings class
- **Responsibilities**:
  - Load environment variables
  - Validate required settings
  - Provide global settings object
  - Configuration documentation

### Documentation Files

#### `README.md`
- **Purpose**: Main project documentation
- **Contains**:
  - Features overview
  - Installation instructions
  - Quick start guide
  - API endpoints reference
  - Configuration options
  - Usage examples
  - Troubleshooting guide

#### `DOCUMENTATION.md`
- **Purpose**: Technical documentation
- **Contains**:
  - Architecture overview
  - System diagrams
  - Module documentation
  - API reference
  - Error handling guide
  - Development guide
  - Performance tuning
  - Deployment guide

#### `QUICKSTART.md`
- **Purpose**: Quick start guide
- **Contains**:
  - Step-by-step setup
  - Testing instructions
  - Troubleshooting tips
  - Configuration examples
  - Complete workflow example

#### `PROJECT_STRUCTURE.md`
- **Purpose**: This file
- **Contains**: Project structure overview and file descriptions

### Configuration Files

#### `.env.example`
- **Purpose**: Example environment variables
- **Use**: Template for creating `.env`
- **Contains**: All configurable options with descriptions

#### `.env` (local, not in repo)
- **Purpose**: Local environment variables
- **Use**: Store sensitive data like API keys
- **Note**: Never commit this file!

#### `requirements.txt`
- **Purpose**: Python dependencies
- **Contains**:
  - All required packages
  - Version specifications
- **Use**: `pip install -r requirements.txt`

### Testing & Examples

#### `test_chatbot.py`
- **Purpose**: Automated test suite
- **Contains**:
  - Health check test
  - Chat endpoint test
  - Context memory test
  - Summarization test
  - Clear conversation test
- **Run**: `python test_chatbot.py`

#### `example_client.py`
- **Purpose**: Example client implementation
- **Contains**:
  - ChatbotClient class
  - Interactive mode
  - Example conversation
- **Run**: `python example_client.py`
- **Features**:
  - Interactive chat
  - Command support (/quit, /clear, /history, /summary)
  - Example conversation mode

### Docker Files

#### `Dockerfile`
- **Purpose**: Docker container configuration
- **Contains**:
  - Python 3.9 base image
  - Dependency installation
  - Port exposure
  - Application startup

#### `docker-compose.yml`
- **Purpose**: Docker Compose orchestration
- **Contains**:
  - Service definition
  - Port mapping
  - Environment variables
  - Container configuration

### Git Files

#### `.gitignore`
- **Purpose**: Exclude files from git
- **Contains**:
  - .env (sensitive data)
  - __pycache__/
  - venv/
  - .DS_Store
  - etc.

## Data Flow

```
1. Client sends request
   ├─ HTTP POST to /chat
   ├─ JSON payload with message & history
   
2. FastAPI validation
   ├─ Pydantic model validation
   ├─ Type checking
   
3. ChatbotService processing
   ├─ Build message list
   ├─ Call OpenAI API
   ├─ Update history
   
4. Response generation
   ├─ Serialize response
   ├─ Include metadata
   
5. Client receives response
   ├─ Parse JSON
   ├─ Update local history
   ├─ Display message
```

## Dependencies Overview

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.104.1 | Web framework |
| uvicorn | 0.24.0 | ASGI server |
| openai | 1.3.6 | OpenAI API client |
| pydantic | 2.5.0 | Data validation |
| python-dotenv | 1.0.0 | Environment variables |
| requests | 2.31.0 | HTTP client |
| aiohttp | 3.9.1 | Async HTTP client |

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | Welcome message |
| GET | /health | Health check |
| GET | /docs | Swagger UI |
| GET | /redoc | ReDoc documentation |
| POST | /chat | Send message |
| POST | /clear | Clear conversation |
| POST | /summarize | Summarize conversation |

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| OPENAI_API_KEY | (required) | OpenAI authentication |
| OPENAI_MODEL | gpt-3.5-turbo | Model selection |
| DEBUG | False | Debug mode |
| HOST | 0.0.0.0 | Server host |
| PORT | 8000 | Server port |
| MAX_TOKENS | 2000 | Max response tokens |
| TEMPERATURE | 0.7 | Response creativity |

## Development Workflow

```
1. Clone/download repository
   
2. Create virtual environment
   python -m venv venv
   source venv/bin/activate
   
3. Install dependencies
   pip install -r requirements.txt
   
4. Setup environment
   cp .env.example .env
   # Edit .env with your API key
   
5. Run development server
   python -m uvicorn app.main:app --reload
   
6. Test the application
   python test_chatbot.py
   or
   python example_client.py
   
7. Access interactive docs
   http://localhost:8000/docs
```

## Deployment Workflow

```
1. Create production .env with:
   - Valid API key
   - DEBUG=False
   - Production settings
   
2. Option A: Direct Python
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   
2. Option B: Docker
   docker build -t chatbot .
   docker run -p 8000:8000 --env-file .env chatbot
   
2. Option C: Docker Compose
   docker-compose up -d
   
3. Verify deployment
   curl http://localhost:8000/health
```

## Common Tasks

### Running the Application
```bash
python -m uvicorn app.main:app --reload
```

### Running Tests
```bash
python test_chatbot.py
```

### Running Example Client
```bash
python example_client.py
```

### Running with Docker
```bash
docker build -t chatbot .
docker run -p 8000:8000 --env-file .env chatbot
```

### Viewing API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Checking Health
```bash
curl http://localhost:8000/health
```

## Key Concepts

### Conversation History
- Maintained on client side
- Sent with each request for context
- Updated with each response
- Enables context-aware responses

### Token Management
- Tracked per request
- Affects cost
- Configurable max tokens
- Lower tokens = faster response

### Error Handling
- Comprehensive error catching
- Informative error messages
- Proper HTTP status codes
- Detailed logging

### Scalability Considerations
- Stateless server design
- Can run multiple instances
- Use load balancer for distribution
- Consider adding caching layer

## Next Steps

1. **Install & Setup**: Follow QUICKSTART.md
2. **Run Application**: Start the server
3. **Test**: Run test_chatbot.py
4. **Explore**: Use interactive docs at /docs
5. **Integrate**: Use example_client.py as reference
6. **Deploy**: Follow deployment instructions in DOCUMENTATION.md

## Support Resources

- **OpenAI API Docs**: https://platform.openai.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Python Requests**: https://requests.readthedocs.io
- **Pydantic**: https://docs.pydantic.dev
