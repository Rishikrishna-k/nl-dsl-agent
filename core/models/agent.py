from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class AgentConfig(BaseModel):
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    instructions: str = Field(..., description="Agent instructions/prompt")
    model: str = Field(default="gpt-4o", description="Model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Model temperature")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens for response")
    tools: Optional[List[str]] = Field(default_factory=list, description="Available tools")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class AgentResponse(BaseModel):
    agent_name: str = Field(..., description="Name of the responding agent")
    content: str = Field(..., description="Response content")
    success: bool = Field(..., description="Whether the response was successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")


class AgentContext(BaseModel):
    session_id: str = Field(..., description="Chat session ID")
    language: str = Field(..., description="Target programming language")
    user_message: str = Field(..., description="User's message")
    chat_history: List[Dict[str, str]] = Field(default_factory=list, description="Chat history")
    examples: Optional[List[Dict[str, Any]]] = Field(None, description="Relevant examples")
    grammar: Optional[str] = Field(None, description="Language grammar")
    max_iterations: int = Field(default=6, description="Maximum agent iterations") 