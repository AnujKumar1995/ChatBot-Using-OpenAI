#!/usr/bin/env python
"""
Simple test script to verify the chatbot is working.
Run this after starting the server to test basic functionality.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health check endpoint."""
    print("\n✓ Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        print(f"  Status: {data['status']}")
        print(f"  Version: {data['version']}")
        print(f"  Model: {data['model']}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_chat():
    """Test chat endpoint."""
    print("\n✓ Testing Chat Endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": "Say 'Hello, this is a test!'",
                "conversation_history": []
            }
        )
        print(f"  Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"  Response: {response.text}")
        assert response.status_code == 200
        data = response.json()
        print(f"  Response: {data['message'][:100]}...")
        print(f"  Tokens used: {data['tokens_used']}")
        print(f"  Model: {data['model']}")
        return True, data["conversation_history"]
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False, []


def test_context(history):
    """Test conversation context."""
    print("\n✓ Testing Conversation Context...")
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": "Do you remember what you just said?",
                "conversation_history": history
            }
        )
        assert response.status_code == 200
        data = response.json()
        print(f"  Response: {data['message'][:100]}...")
        print(f"  History length: {len(data['conversation_history'])} messages")
        return True, data["conversation_history"]
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False, history


def test_summarize(history):
    """Test conversation summarization."""
    print("\n✓ Testing Conversation Summarization...")
    try:
        response = requests.post(
            f"{BASE_URL}/summarize",
            json={"conversation_history": history}
        )
        assert response.status_code == 200
        data = response.json()
        print(f"  Summary: {data['summary']}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_clear():
    """Test clear endpoint."""
    print("\n✓ Testing Clear Conversation...")
    try:
        response = requests.post(f"{BASE_URL}/clear")
        assert response.status_code == 200
        data = response.json()
        print(f"  Message: {data['message']}")
        print(f"  History: {data['history']}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("OpenAI Chatbot API - Test Suite")
    print("=" * 60)
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to server!")
        print(f"  Make sure the server is running at {BASE_URL}")
        print("\n  Start the server with:")
        print("  python -m uvicorn app.main:app --reload")
        sys.exit(1)
    
    # Run tests
    results = []
    
    results.append(("Health Check", test_health()))
    chat_ok, history = test_chat()
    results.append(("Chat Endpoint", chat_ok))
    
    if chat_ok:
        context_ok, history = test_context(history)
        results.append(("Context Memory", context_ok))
        
        if context_ok:
            results.append(("Summarization", test_summarize(history)))
    
    results.append(("Clear Conversation", test_clear()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} | {test_name}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n✓ All tests passed! The chatbot is working correctly.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
