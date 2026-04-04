# OpenAI Chatbot API

A FastAPI-based web application that provides a RESTful API for interacting with OpenAI's language models. This chatbot maintains conversation history and provides context-aware responses.

## Features

✨ **Key Features:**
- **FastAPI Backend**: Modern, fast Python web framework with automatic API documentation
- **OpenAI Integration**: Uses OpenAI's GPT models for intelligent responses
- **Conversation Memory**: Maintains conversation history for context-aware responses
- **RESTful API**: Clean, well-documented API endpoints
- **Error Handling**: Comprehensive error handling and logging
- **CORS Support**: Cross-origin resource sharing enabled
- **Health Checks**: Built-in health check endpoint
- **Conversation Management**: Clear conversations and generate summaries

## Project Structure

```
ChatBot Using OpenAI/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py              # FastAPI application
│   ├── chatbot.py           # ChatbotService class
│   └── models.py            # Pydantic models
├── config/
│   └── settings.py          # Configuration settings
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- OpenAI API key (get one from https://platform.openai.com/api-keys)

### Setup Steps

1. **Clone/Download the project:**
   ```bash
   cd "ChatBot Using OpenAI"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

### Start the server:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Access the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model": "gpt-3.5-turbo"
}
```

### 2. Send Message
```http
POST /chat
Content-Type: application/json

{
  "message": "What is Python?",
  "conversation_history": []
}
```

**Response:**
```json
{
  "message": "Python is a high-level programming language...",
  "conversation_history": [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a high-level programming language..."}
  ],
  "model": "gpt-3.5-turbo",
  "tokens_used": 45
}
```

### 3. Clear Conversation
```http
POST /clear
```

### 4. Summarize Conversation
```http
POST /summarize
Content-Type: application/json

{
  "conversation_history": [
    {"role": "user", "content": "Tell me about machine learning"},
    {"role": "assistant", "content": "Machine learning is..."}
  ]
}
```

## Configuration

Edit `.env` file to customize settings:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here     # Your OpenAI API key (required)
OPENAI_MODEL=gpt-3.5-turbo           # Model to use (default: gpt-3.5-turbo)

# Application Configuration
DEBUG=True                             # Enable debug mode
HOST=0.0.0.0                          # Server host
PORT=8000                             # Server port
MAX_TOKENS=2000                       # Max tokens per response
TEMPERATURE=0.7                       # Response creativity (0-2)
```

### Configuration Options Explained:

- **OPENAI_API_KEY**: Required. Your OpenAI API key for authentication.
- **OPENAI_MODEL**: The ChatGPT model to use. Options: `gpt-3.5-turbo`, `gpt-4`, etc.
- **MAX_TOKENS**: Maximum tokens in the response (higher = longer responses)
- **TEMPERATURE**: Controls randomness. 0 = deterministic, 2 = very random

## Usage Examples

### Python Example
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Initialize conversation
conversation_history = []

def chat(message):
    global conversation_history
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": message,
            "conversation_history": conversation_history
        }
    )
    
    data = response.json()
    conversation_history = data["conversation_history"]
    return data["message"]

# Use the chatbot
print(chat("Hello, how are you?"))
print(chat("What's your name?"))  # Context-aware response
```

### cURL Example
```bash
# Send a message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is FastAPI?",
    "conversation_history": []
  }'

# Check health
curl "http://localhost:8000/health"

# Clear conversation
curl -X POST "http://localhost:8000/clear"
```

### JavaScript/Fetch Example
```javascript
async function sendMessage(message, history = []) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      conversation_history: history
    })
  });
  
  return await response.json();
}

// Usage
const result = await sendMessage("Tell me a joke");
console.log(result.message);
```

## Code Documentation

### ChatbotService Class
Main service for interacting with OpenAI API.

**Methods:**
- `send_message(user_message, conversation_history)`: Send a message and get a response
- `clear_conversation()`: Clear conversation history
- `get_conversation_summary(conversation_history)`: Generate a summary

### Models

#### ChatRequest
Request model with:
- `message`: The user's message
- `conversation_history`: Optional previous messages

#### ChatResponse
Response model with:
- `message`: The chatbot's response
- `conversation_history`: Updated history
- `model`: Model used
- `tokens_used`: Tokens consumed

## Error Handling

The API handles various errors gracefully:

| Error | Status | Description |
|-------|--------|-------------|
| Invalid API Key | 500 | OpenAI API key is invalid |
| Rate Limit | 500 | OpenAI API rate limit exceeded |
| Validation Error | 400 | Invalid request format |
| Server Error | 500 | Unexpected server error |

## Requirements

- **fastapi** (0.104.1): Web framework
- **uvicorn** (0.24.0): ASGI server
- **openai** (1.3.6): OpenAI API client
- **python-dotenv** (1.0.0): Environment variable management
- **pydantic** (2.5.0): Data validation
- **requests** (2.31.0): HTTP client
- **aiohttp** (3.9.1): Async HTTP client

See `requirements.txt` for complete list.

## Deployment

### Using Docker (Example)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Heroku
```bash
heroku create your-app-name
git push heroku main
heroku config:set OPENAI_API_KEY=your_key_here
```

## Troubleshooting

### Issue: "OPENAI_API_KEY is not set"
**Solution**: Make sure you have created a `.env` file and added your API key:
```bash
cp .env.example .env
# Edit .env and add your key
```

### Issue: "Invalid API Key"
**Solution**: Verify your API key is correct from https://platform.openai.com/api-keys

### Issue: "Rate limit exceeded"
**Solution**: Wait a moment and try again. OpenAI API has rate limits.

### Issue: ModuleNotFoundError
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## API Response Examples

### Successful Response
```json
{
  "message": "Python is a versatile programming language...",
  "conversation_history": [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a versatile..."}
  ],
  "model": "gpt-3.5-turbo",
  "tokens_used": 156
}
```

### Error Response
```json
{
  "detail": "Invalid OpenAI API key"
}
```

## Performance Considerations

- **Conversation History**: Longer conversations consume more tokens
- **Max Tokens**: Higher values increase response time and cost
- **Temperature**: Lower values are faster, higher values are more creative
- **Token Counting**: The API returns `tokens_used` for cost tracking

## Security Considerations

1. **API Key Management**: Never commit `.env` file with real keys
2. **CORS**: Currently allows all origins. Restrict in production
3. **Rate Limiting**: Consider adding rate limiting for production
4. **Input Validation**: All inputs are validated using Pydantic

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review OpenAI API documentation: https://platform.openai.com/docs
3. Check FastAPI documentation: https://fastapi.tiangolo.com

## References

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Uvicorn Documentation](https://www.uvicorn.org)
