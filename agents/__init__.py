from .base_agent import BaseAgent
from .langchain_agent import LangChainAgent
from .custom_agent import CustomAgent

def MyAgent(backend='langchain', **kwargs):
    """Factory function to create the appropriate agent type."""
    if backend == 'langchain':
        return LangChainAgent(**kwargs)
    elif backend == 'custom':
        return CustomAgent(**kwargs)
    else:
        raise ValueError(f"Unknown backend: {backend}")

__all__ = ['BaseAgent', 'LangChainAgent', 'CustomAgent', 'MyAgent'] 