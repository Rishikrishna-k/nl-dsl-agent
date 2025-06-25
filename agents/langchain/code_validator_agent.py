from .langchain_agent import LangChainAgent

class CodeValidatorAgent(LangChainAgent):
    """Specialized agent for code validation, extends LangChainAgent."""
    def __init__(self, llm, tools=None, memory=None, agent_type=None, verbose=True, **kwargs):
        super().__init__(llm, tools, memory, agent_type, verbose, **kwargs)
        # Add any validator-specific setup here if needed

    # Optionally override query() or add validator-specific methods 
    