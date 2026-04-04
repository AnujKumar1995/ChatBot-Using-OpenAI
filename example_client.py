"""
Example client application showing how to use the chatbot API.
Run the server first: python -m uvicorn app.main:app --reload
Then run this: python example_client.py
"""

import requests
import json
import sys
from typing import List, Dict


class ChatbotClient:
    """Client for interacting with the chatbot API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the client."""
        self.base_url = base_url
        self.conversation_history: List[Dict] = []
    
    def chat(self, message: str) -> str:
        """Send a message and get a response."""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": message,
                    "conversation_history": self.conversation_history
                }
            )
            
            if response.status_code != 200:
                print(f"Error: {response.json()['detail']}")
                return None
            
            data = response.json()
            self.conversation_history = data["conversation_history"]
            
            return data["message"]
        
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to server. Is it running?")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def summarize(self) -> str:
        """Get a summary of the conversation."""
        if not self.conversation_history:
            return "No conversation to summarize"
        
        try:
            response = requests.post(
                f"{self.base_url}/summarize",
                json={"conversation_history": self.conversation_history}
            )
            
            data = response.json()
            return data["summary"]
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def clear(self):
        """Clear the conversation history."""
        try:
            requests.post(f"{self.base_url}/clear")
            self.conversation_history = []
            print("Conversation cleared!")
        except Exception as e:
            print(f"Error: {e}")
    
    def show_history(self):
        """Display conversation history."""
        if not self.conversation_history:
            print("No conversation history yet.")
            return
        
        print("\nConversation History:")
        print("-" * 60)
        for msg in self.conversation_history:
            role = msg["role"].capitalize()
            content = msg["content"]
            print(f"{role}: {content}\n")
        print("-" * 60)


def interactive_mode():
    """Interactive chat mode."""
    print("\n" + "=" * 60)
    print("OpenAI Chatbot - Interactive Mode")
    print("=" * 60)
    print("Commands:")
    print("  /quit    - Exit the chat")
    print("  /clear   - Clear conversation history")
    print("  /history - Show conversation history")
    print("  /summary - Summarize the conversation")
    print("-" * 60 + "\n")
    
    client = ChatbotClient()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "/quit":
                print("Goodbye!")
                break
            elif user_input.lower() == "/clear":
                client.clear()
                continue
            elif user_input.lower() == "/history":
                client.show_history()
                continue
            elif user_input.lower() == "/summary":
                summary = client.summarize()
                print(f"\nSummary: {summary}\n")
                continue
            
            # Send message
            response = client.chat(user_input)
            if response:
                print(f"Bot: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


def example_conversation():
    """Run an example conversation."""
    print("\n" + "=" * 60)
    print("OpenAI Chatbot - Example Conversation")
    print("=" * 60 + "\n")
    
    client = ChatbotClient()
    
    # Example messages
    messages = [
        "What is machine learning?",
        "What are its main applications?",
        "How is it different from deep learning?",
    ]
    
    for msg in messages:
        print(f"You: {msg}")
        response = client.chat(msg)
        if response:
            print(f"Bot: {response}\n")
        else:
            print("Failed to get response.\n")
    
    # Show summary
    print("-" * 60)
    print("Generating summary...")
    summary = client.summarize()
    print(f"Summary: {summary}\n")


def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        example_conversation()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
