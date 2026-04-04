# API Usage Examples

This file contains practical examples of how to use the ChatBot API.

## cURL Examples

### 1. Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model": "gpt-3.5-turbo"
}
```

### 2. Send a Simple Message
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Python?",
    "conversation_history": []
  }'
```

**Response:**
```json
{
  "message": "Python is a high-level, interpreted programming language...",
  "conversation_history": [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a high-level..."}
  ],
  "model": "gpt-3.5-turbo",
  "tokens_used": 87
}
```

### 3. Multi-turn Conversation
```bash
# First message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about machine learning",
    "conversation_history": []
  }' > response1.json

# Extract history from response and use in next request
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are its applications?",
    "conversation_history": [
      {"role": "user", "content": "Tell me about machine learning"},
      {"role": "assistant", "content": "Machine learning is..."}
    ]
  }'
```

### 4. Clear Conversation
```bash
curl -X POST "http://localhost:8000/clear"
```

**Response:**
```json
{
  "message": "Conversation cleared",
  "history": []
}
```

### 5. Summarize Conversation
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_history": [
      {"role": "user", "content": "What is AI?"},
      {"role": "assistant", "content": "AI is artificial intelligence..."},
      {"role": "user", "content": "What about ML?"},
      {"role": "assistant", "content": "ML is machine learning..."}
    ]
  }'
```

**Response:**
```json
{
  "summary": "The conversation covered the basics of AI and machine learning, explaining that AI is the broader field of artificial intelligence while ML is a specific subset..."
}
```

---

## Python Examples

### 1. Simple Request
```python
import requests

response = requests.post(
    'http://localhost:8000/chat',
    json={
        'message': 'What is FastAPI?',
        'conversation_history': []
    }
)

print(response.json()['message'])
```

### 2. Maintaining Conversation History
```python
import requests

BASE_URL = 'http://localhost:8000'

def chat(message, history):
    response = requests.post(
        f'{BASE_URL}/chat',
        json={
            'message': message,
            'conversation_history': history
        }
    )
    data = response.json()
    return data['message'], data['conversation_history']

# Start conversation
history = []
response, history = chat('Hello!', history)
print(f"Bot: {response}\n")

# Follow-up with context
response, history = chat('What is your name?', history)
print(f"Bot: {response}\n")

# Another question with context
response, history = chat('Can you help me learn Python?', history)
print(f"Bot: {response}\n")
```

### 3. Using the Client Class
```python
from example_client import ChatbotClient

client = ChatbotClient()

# Send messages
response1 = client.chat("Tell me a joke")
print(response1)

response2 = client.chat("Tell me another one")
print(response2)

# Get summary
summary = client.summarize()
print(f"Summary: {summary}")

# Clear history
client.clear()
```

### 4. Error Handling
```python
import requests

def safe_chat(message, history=None):
    try:
        if history is None:
            history = []
        
        response = requests.post(
            'http://localhost:8000/chat',
            json={
                'message': message,
                'conversation_history': history
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return True, data['message'], data['conversation_history']
        else:
            error = response.json().get('detail', 'Unknown error')
            return False, error, history
    
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to server", history
    except requests.exceptions.Timeout:
        return False, "Request timeout", history
    except Exception as e:
        return False, str(e), history

# Usage
success, message, history = safe_chat("Hello!")
if success:
    print(f"Bot: {message}")
else:
    print(f"Error: {message}")
```

### 5. Token Tracking
```python
import requests

total_tokens = 0
conversations = []

response = requests.post(
    'http://localhost:8000/chat',
    json={
        'message': 'Explain quantum computing in 2 sentences',
        'conversation_history': []
    }
)

data = response.json()
tokens_used = data['tokens_used']
total_tokens += tokens_used

print(f"Tokens used: {tokens_used}")
print(f"Total tokens: {total_tokens}")

# Estimate cost (GPT-3.5-turbo: $0.0005 per 1K tokens)
cost = (total_tokens / 1000) * 0.0005
print(f"Estimated cost: ${cost:.6f}")
```

---

## JavaScript/Fetch Examples

### 1. Basic Request
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
sendMessage('Hello!').then(data => {
    console.log(data.message);
    console.log(`Tokens: ${data.tokens_used}`);
});
```

### 2. Conversation with History
```javascript
class ChatbotClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
        this.history = [];
    }
    
    async chat(message) {
        const response = await fetch(`${this.baseUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_history: this.history
            })
        });
        
        const data = await response.json();
        this.history = data.conversation_history;
        return data.message;
    }
    
    async summarize() {
        const response = await fetch(`${this.baseUrl}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                conversation_history: this.history
            })
        });
        
        const data = await response.json();
        return data.summary;
    }
}

// Usage
const bot = new ChatbotClient();
const msg1 = await bot.chat('What is AI?');
const msg2 = await bot.chat('Tell me about machine learning');
const summary = await bot.summarize();
```

### 3. With React
```jsx
import { useState } from 'react';

function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [history, setHistory] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    
    const handleSend = async () => {
        if (!input.trim()) return;
        
        setLoading(true);
        setMessages([...messages, { role: 'user', content: input }]);
        
        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: input,
                    conversation_history: history
                })
            });
            
            const data = await response.json();
            setHistory(data.conversation_history);
            setMessages(prev => [
                ...prev,
                { role: 'assistant', content: data.message }
            ]);
        } catch (error) {
            console.error('Error:', error);
        }
        
        setInput('');
        setLoading(false);
    };
    
    return (
        <div className="chat-app">
            <div className="messages">
                {messages.map((msg, i) => (
                    <div key={i} className={`message ${msg.role}`}>
                        {msg.content}
                    </div>
                ))}
            </div>
            <div className="input-area">
                <input
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyPress={e => e.key === 'Enter' && handleSend()}
                    placeholder="Type a message..."
                />
                <button onClick={handleSend} disabled={loading}>
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </div>
        </div>
    );
}
```

---

## Advanced Examples

### 1. Rate Limiting Implementation
```python
from datetime import datetime, timedelta
from functools import wraps

class RateLimiter:
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
    
    def is_allowed(self):
        now = datetime.now()
        # Remove old requests outside window
        self.requests = [
            req_time for req_time in self.requests
            if now - req_time < timedelta(seconds=self.window_seconds)
        ]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False

limiter = RateLimiter(max_requests=5, window_seconds=60)

def chat_with_limit(message, history):
    if not limiter.is_allowed():
        return None, "Rate limit exceeded"
    
    response = requests.post(
        'http://localhost:8000/chat',
        json={'message': message, 'conversation_history': history}
    )
    return response.json()
```

### 2. Persistent Chat History
```python
import json
from pathlib import Path

class PersistentChatbot:
    def __init__(self, history_file='chat_history.json'):
        self.history_file = Path(history_file)
        self.history = self._load_history()
    
    def _load_history(self):
        if self.history_file.exists():
            with open(self.history_file) as f:
                return json.load(f)
        return []
    
    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)
    
    def chat(self, message):
        response = requests.post(
            'http://localhost:8000/chat',
            json={'message': message, 'conversation_history': self.history}
        )
        
        data = response.json()
        self.history = data['conversation_history']
        self._save_history()
        return data['message']

bot = PersistentChatbot()
print(bot.chat("Hello"))
# History is saved to chat_history.json
```

### 3. Batch Processing
```python
import requests
from typing import List

def batch_chat(messages: List[str]) -> List[str]:
    """Process multiple messages in sequence with context."""
    history = []
    responses = []
    
    for message in messages:
        response = requests.post(
            'http://localhost:8000/chat',
            json={'message': message, 'conversation_history': history}
        )
        
        data = response.json()
        history = data['conversation_history']
        responses.append(data['message'])
    
    return responses

# Process multiple questions
questions = [
    "What is Python?",
    "What are its main features?",
    "How do I install it?",
    "Show me a simple example"
]

answers = batch_chat(questions)
for q, a in zip(questions, answers):
    print(f"Q: {q}")
    print(f"A: {a}\n")
```

---

## Testing Examples

### Using unittest
```python
import unittest
import requests

class TestChatAPI(unittest.TestCase):
    BASE_URL = 'http://localhost:8000'
    
    def test_health_check(self):
        response = requests.get(f'{self.BASE_URL}/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'healthy')
    
    def test_chat_endpoint(self):
        response = requests.post(
            f'{self.BASE_URL}/chat',
            json={'message': 'Hello', 'conversation_history': []}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertIn('tokens_used', response.json())
    
    def test_conversation_context(self):
        # First message
        resp1 = requests.post(
            f'{self.BASE_URL}/chat',
            json={'message': 'My name is John', 'conversation_history': []}
        )
        history = resp1.json()['conversation_history']
        
        # Second message should remember name
        resp2 = requests.post(
            f'{self.BASE_URL}/chat',
            json={'message': 'What is my name?', 'conversation_history': history}
        )
        response_text = resp2.json()['message'].lower()
        self.assertIn('john', response_text)

if __name__ == '__main__':
    unittest.main()
```

---

## Common Patterns

### Pattern 1: Simple Q&A
```python
response = requests.post('http://localhost:8000/chat', json={
    'message': 'What is the capital of France?',
    'conversation_history': []
})
print(response.json()['message'])
```

### Pattern 2: Multi-turn Dialog
```python
history = []
messages = ['Hi', 'How are you?', 'Can you help?', 'Thank you!']

for msg in messages:
    resp = requests.post('http://localhost:8000/chat', json={
        'message': msg,
        'conversation_history': history
    })
    history = resp.json()['conversation_history']
    print(resp.json()['message'])
```

### Pattern 3: Async Processing
```python
import asyncio
import aiohttp

async def async_chat(message, history):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:8000/chat',
            json={'message': message, 'conversation_history': history}
        ) as resp:
            return await resp.json()

async def main():
    history = []
    for msg in ['Hello', 'How are you?']:
        data = await async_chat(msg, history)
        history = data['conversation_history']
        print(data['message'])

asyncio.run(main())
```

---

For more examples and detailed usage, see the `example_client.py` file!
