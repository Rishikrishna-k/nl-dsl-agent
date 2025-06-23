from fastapi import FastAPI, Depends
from pydantic import BaseModel
from config.settings import get_settings, Settings
from app.openrouter_client import get_openrouter_client

app = FastAPI(title="DSL LangChain API", version="0.1.0")

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    result: str
    metadata: dict | None = None

@app.get("/")
def root():
    return {"message": "Welcome to the DSL LangChain API!"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/generate", response_model=GenerateResponse)
def generate(
    request: GenerateRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Generate code or text based on the input prompt using OpenRouter and the configured model.
    """
    client = get_openrouter_client()
    model = settings.LLM_MODEL
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        )
        result = completion.choices[0].message.content
    except Exception as e:
        result = f"[ERROR] {str(e)}"
    return GenerateResponse(
        result=result,
        metadata={
            "model": model
        }
    ) 