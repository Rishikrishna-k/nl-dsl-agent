from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class AzureOpenAIConfig(BaseModel):
    endpoint: str = Field(..., description="Azure OpenAI endpoint")
    api_key: str = Field(..., description="Azure OpenAI API key")
    api_version: str = Field(default="2024-02-15-preview", description="Azure OpenAI API version")
    deployment_name: str = Field(default="gpt-4o", description="Azure OpenAI deployment name")


class AzureSearchConfig(BaseModel):
    endpoint: str = Field(..., description="Azure AI Search endpoint")
    api_key: str = Field(..., description="Azure AI Search API key")
    index_name: str = Field(default="dsl-examples", description="Azure AI Search index name")


class AzureStorageConfig(BaseModel):
    connection_string: str = Field(..., description="Azure Storage connection string")
    container_name: str = Field(default="dsl-documents", description="Azure Storage container name")


class AppConfig(BaseModel):
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Application environment")
    debug: bool = Field(default=False, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Application host")
    port: int = Field(default=8000, description="Application port")
    secret_key: str = Field(..., description="Application secret key")
    session_timeout: int = Field(default=3600, description="Session timeout in seconds")
    log_level: str = Field(default="INFO", description="Log level")
    
    # Azure configurations
    azure_openai: AzureOpenAIConfig
    azure_search: Optional[AzureSearchConfig] = None
    azure_storage: Optional[AzureStorageConfig] = None 