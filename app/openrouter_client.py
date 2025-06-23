from openai import OpenAI
from config.settings import get_settings

def get_openrouter_client():
    settings = get_settings()
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,
    ) 