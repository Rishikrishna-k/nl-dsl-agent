from app.context.context import Context
from agents.langchain.code_generator_agent import CodeGeneratorAgent
from agents.langchain.code_validator_agent import CodeValidatorAgent
from agents.langchain.langchain_agent import LangChainAgent
from app.openrouter_client import OpenRouterClient  # if this class exists

try:
    import fastapi
    print("fastapi: OK")
except ImportError as e:
    print(f"fastapi: FAIL - {e}")

try:
    import uvicorn
    print("uvicorn: OK")
except ImportError as e:
    print(f"uvicorn: FAIL - {e}")

try:
    import pydantic
    print("pydantic: OK")
except ImportError as e:
    print(f"pydantic: FAIL - {e}")

try:
    import langchain
    print("langchain: OK")
except ImportError as e:
    print(f"langchain: FAIL - {e}")

try:
    import langgraph
    print("langgraph: OK")
except ImportError as e:
    print(f"langgraph: FAIL - {e}")

try:
    import openai
    print("openai: OK")
except ImportError as e:
    print(f"openai: FAIL - {e}")

try:
    import tiktoken
    print("tiktoken: OK")
except ImportError as e:
    print(f"tiktoken: FAIL - {e}")

try:
    import chromadb
    print("chromadb: OK")
except ImportError as e:
    print(f"chromadb: FAIL - {e}")

try:
    import faiss
    print("faiss: OK")
except ImportError as e:
    print(f"faiss: FAIL - {e}")

try:
    import yaml
    print("pyyaml: OK")
except ImportError as e:
    print(f"pyyaml: FAIL - {e}")

try:
    import dotenv
    print("python-dotenv: OK")
except ImportError as e:
    print(f"python-dotenv: FAIL - {e}")

try:
    import httpx
    print("httpx: OK")
except ImportError as e:
    print(f"httpx: FAIL - {e}")

try:
    import requests
    print("requests: OK")
except ImportError as e:
    print(f"requests: FAIL - {e}")

try:
    import rich
    print("rich: OK")
except ImportError as e:
    print(f"rich: FAIL - {e}")

try:
    import pytest
    print("pytest: OK")
except ImportError as e:
    print(f"pytest: FAIL - {e}")

try:
    import black
    print("black: OK")
except ImportError as e:
    print(f"black: FAIL - {e}")

try:
    import isort
    print("isort: OK")
except ImportError as e:
    print(f"isort: FAIL - {e}")

try:
    import mypy
    print("mypy: OK")
except ImportError as e:
    print(f"mypy: FAIL - {e}")

try:
    import docker
    print("docker: OK")
except ImportError as e:
    print(f"docker: FAIL - {e}")

try:
    import antlr4
    print("antlr4-python3-runtime: OK")
except ImportError as e:
    print(f"antlr4-python3-runtime: FAIL - {e}") 