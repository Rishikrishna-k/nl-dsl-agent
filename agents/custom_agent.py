from .base_agent import BaseAgent

class CustomAgent(BaseAgent):
    """Custom agent implementation."""
    def __init__(self, llm, tools=None, memory=None, agent_type=None, verbose=True, **kwargs):
        super().__init__(llm, tools, memory, agent_type, verbose, **kwargs)
        from agents.code_generator_agent import CodeGeneratorAgent
        self._executor = CodeGeneratorAgent(**self.extra_config)

    def query(self, query, prompt=None, context=None):
        if self._executor is None:
            raise RuntimeError("Agent not initialized.")
        return self._executor.run(query, prompt=prompt, context=context) 