import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from core.models.config import AppConfig, AzureOpenAIConfig
from core.services.chat_service import ChatService
from core.services.example_service import ExampleService
from core.services.grammar_service import GrammarService
from core.agents.agent_factory import AgentFactory
from core.services.dsl_ai_service import DslAIService
from app.routes import chat, api


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting DSL Copilot application...")
    
    # Initialize services
    app.state.chat_service = ChatService()
    app.state.example_service = ExampleService()
    app.state.grammar_service = GrammarService()
    app.state.agent_factory = AgentFactory()
    app.state.dsl_ai_service = DslAIService(
        chat_service=app.state.chat_service,
        agent_factory=app.state.agent_factory
    )
    
    logger.info("DSL Copilot application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down DSL Copilot application...")


# Create FastAPI app
app = FastAPI(
    title="DSL Copilot",
    description="AI-powered code generation for Domain-Specific Languages",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(api.router, prefix="/api", tags=["api"])


@app.get("/")
async def root(request: Request):
    """Root endpoint - redirect to chat interface"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "chat_service": "running",
            "example_service": "running",
            "grammar_service": "running",
            "agent_factory": "running",
            "dsl_ai_service": "running"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {
        "error": "Internal server error",
        "message": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else "An error occurred"
    }


if __name__ == "__main__":
    import uvicorn
    
    config = AppConfig(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        secret_key=os.getenv("SECRET_KEY", "your-secret-key-here"),
        azure_openai=AzureOpenAIConfig(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        )
    )
    
    uvicorn.run(
        "app.main:app",
        host=config.host,
        port=config.port,
        reload=config.debug,
        log_level=config.log_level.lower()
    ) 