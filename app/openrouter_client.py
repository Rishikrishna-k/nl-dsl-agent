from openai import OpenAI
from config.settings import get_settings
from langchain_openai import ChatOpenAI

def get_openrouter_client():
    settings = get_settings()
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,
    )

def get_openrouter_api_key():
    settings = get_settings()
    return settings.OPENROUTER_API_KEY

def get_openrouter_llm(model: str = "deepseek/deepseek-r1:free", temperature: float = 0.7):
    settings = get_settings()
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key=settings.OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1"
    )