from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

# Load .env file explicitly
load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    LLM_MODEL: str = ""
    DEBUG: bool = False
    APP_NAME: str = "DSL LangChain API"
    API_PORT: int = 8000  # Port for FastAPI app
    # Add DB config fields here later (e.g., DATABASE_URL)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"🔧 Settings loaded:")
    print(f"   OPENROUTER_API_KEY: {'***' if settings.OPENROUTER_API_KEY else 'NOT SET'}")
    print(f"   LLM_MODEL: {settings.LLM_MODEL}")
    print(f"   DEBUG: {settings.DEBUG}")
    return settings 