"""Configuration settings for the chatbot application."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Application metadata
    APP_NAME: str = "OpenAI Chatbot API"
    APP_VERSION: str = "1.0.0"
    
    def validate(self):
        """Validate required settings."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set. Please set it in .env file")


settings = Settings()
settings.validate()
