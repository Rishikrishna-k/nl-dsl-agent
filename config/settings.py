from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    LLM_MODEL: str = "mistralai/mistral-7b-instruct"
    DEBUG: bool = False
    APP_NAME: str = "DSL LangChain API"
    API_PORT: int = 8000  # Port for FastAPI app
    # Add DB config fields here later (e.g., DATABASE_URL)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings() 