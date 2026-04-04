"""
QUICKSTART GUIDE FOR OpenAI CHATBOT API

This guide will get you up and running in 5 minutes.
"""

# ==============================================================================
# STEP 1: INSTALL PYTHON & DEPENDENCIES
# ==============================================================================

# Make sure you have Python 3.8+ installed
# python --version

# Install dependencies:
# pip install -r requirements.txt


# ==============================================================================
# STEP 2: GET YOUR OPENAI API KEY
# ==============================================================================

# 1. Go to https://platform.openai.com/api-keys
# 2. Create a new API key
# 3. Copy your key


# ==============================================================================
# STEP 3: SETUP ENVIRONMENT
# ==============================================================================

# Create .env file from template:
# cp .env.example .env

# Edit .env and add your API key:
# OPENAI_API_KEY=sk-...


# ==============================================================================
# STEP 4: RUN THE SERVER
# ==============================================================================

# In your terminal, run:
# python -m uvicorn app.main:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete


# ==============================================================================
# STEP 5: TEST THE API
# ==============================================================================

# Option A: Use Swagger UI (Easiest)
# - Open browser: http://localhost:8000/docs
# - Click on POST /chat
# - Click "Try it out"
# - Enter your message
# - Click "Execute"

# Option B: Use cURL
# curl -X POST http://localhost:8000/chat \
#   -H "Content-Type: application/json" \
#   -d '{"message":"Hello! How are you?","conversation_history":[]}'

# Option C: Use Python
"""
import requests

response = requests.post(
    'http://localhost:8000/chat',
    json={
        'message': 'Hello! How are you?',
        'conversation_history': []
    }
)

print(response.json()['message'])
"""


# ==============================================================================
# STEP 6: MAINTAIN CONVERSATION HISTORY
# ==============================================================================

# Save conversation history from previous response
# Send it with your next message for context

"""
# Example conversation flow:

# Message 1
response1 = requests.post(
    'http://localhost:8000/chat',
    json={
        'message': 'What is Python?',
        'conversation_history': []
    }
)
history = response1.json()['conversation_history']
print(response1.json()['message'])

# Message 2 (with context from Message 1)
response2 = requests.post(
    'http://localhost:8000/chat',
    json={
        'message': 'What are its main features?',
        'conversation_history': history  # Pass previous messages
    }
)
history = response2.json()['conversation_history']
print(response2.json()['message'])
"""


# ==============================================================================
# STEP 7: USEFUL ENDPOINTS
# ==============================================================================

# Health Check
# GET http://localhost:8000/health

# Chat
# POST http://localhost:8000/chat

# Clear Conversation
# POST http://localhost:8000/clear

# Summarize Conversation
# POST http://localhost:8000/summarize

# Interactive API Docs
# http://localhost:8000/docs


# ==============================================================================
# TROUBLESHOOTING
# ==============================================================================

# Q: "OPENAI_API_KEY is not set"
# A: Make sure you have .env file with your API key
#    cp .env.example .env
#    # Edit .env and add your key

# Q: "Invalid OpenAI API key"
# A: Check your API key at https://platform.openai.com/api-keys

# Q: "Module not found" error
# A: Install dependencies:
#    pip install -r requirements.txt

# Q: "Connection refused"
# A: Make sure server is running:
#    python -m uvicorn app.main:app --reload

# Q: "Rate limit exceeded"
# A: OpenAI API has rate limits. Wait a moment and try again.


# ==============================================================================
# CONFIGURATION TIPS
# ==============================================================================

# In .env file, you can customize:

# OPENAI_MODEL=gpt-3.5-turbo
# Options: gpt-3.5-turbo (fast, cheap) or gpt-4 (slower, smarter)

# MAX_TOKENS=2000
# Higher = longer responses (costs more)

# TEMPERATURE=0.7
# 0 = predictable, 1 = creative, 2 = very random

# DEBUG=True
# Set to False in production


# ==============================================================================
# EXAMPLE COMPLETE WORKFLOW
# ==============================================================================

"""
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Start conversation
print("Starting chatbot conversation...")

# 2. Send first message
msg1 = requests.post(f"{BASE_URL}/chat", json={
    "message": "Who was Albert Einstein?",
    "conversation_history": []
})

response1 = msg1.json()
history = response1["conversation_history"]
print(f"Bot: {response1['message']}\n")

# 3. Ask follow-up (context-aware)
msg2 = requests.post(f"{BASE_URL}/chat", json={
    "message": "What are his most important contributions?",
    "conversation_history": history
})

response2 = msg2.json()
history = response2["conversation_history"]
print(f"Bot: {response2['message']}\n")

# 4. Ask another question
msg3 = requests.post(f"{BASE_URL}/chat", json={
    "message": "When did he die?",
    "conversation_history": history
})

response3 = msg3.json()
history = response3["conversation_history"]
print(f"Bot: {response3['message']}\n")

# 5. Get summary
summary = requests.post(f"{BASE_URL}/summarize", json={
    "conversation_history": history
})

print(f"Summary: {summary.json()['summary']}\n")

# 6. Clear conversation
requests.post(f"{BASE_URL}/clear")
print("Conversation cleared!")
"""


# ==============================================================================
# NEXT STEPS
# ==============================================================================

# 1. Read README.md for complete documentation
# 2. Read DOCUMENTATION.md for technical details
# 3. Explore the code in app/ directory
# 4. Try different prompts and see how it responds
# 5. Integrate it with your application
