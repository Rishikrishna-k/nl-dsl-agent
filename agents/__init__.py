from .base_agent import BaseAgent
from .langchain.langchain_agent import LangChainAgent
from .langchain.code_generator_agent import CodeGeneratorAgent
from .langchain.code_validator_agent import CodeValidatorAgent
from .custom_agent import CustomAgent

def MyAgent(backend='langchain', **kwargs):
    """Factory function to create the appropriate agent type."""
    if backend == 'langchain':
        return LangChainAgent(**kwargs)
    elif backend == 'codegen':
        return CodeGeneratorAgent(**kwargs)
    elif backend == 'validator':
        return CodeValidatorAgent(**kwargs)
    elif backend == 'custom':
        return CustomAgent(**kwargs)
    else:
        raise ValueError(f"Unknown backend: {backend}")

__all__ = ['BaseAgent', 'LangChainAgent', 'CodeGeneratorAgent', 'CodeValidatorAgent', 'CustomAgent', 'MyAgent'] 