"""Configuration settings for the chatbot application."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_FINE_TUNED_MODEL: str = os.getenv("OPENAI_FINE_TUNED_MODEL", "")

    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))

    # Customer support config
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Our Company")

    # Application metadata
    APP_NAME: str = "Customer Support Chatbot API"
    APP_VERSION: str = "2.0.0"

    @property
    def active_model(self) -> str:
        """Return fine-tuned model if set, else default model."""
        return self.OPENAI_FINE_TUNED_MODEL or self.OPENAI_MODEL

    def validate(self):
        """Validate required settings."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set. Please set it in .env file")


settings = Settings()
settings.validate()
