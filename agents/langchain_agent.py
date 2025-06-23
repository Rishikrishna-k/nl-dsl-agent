from .base_agent import BaseAgent

class LangChainAgent(BaseAgent):
    """LangChain agent implementation."""
    def __init__(self, llm, tools=None, memory=None, agent_type=None, verbose=True, **kwargs):
        super().__init__(llm, tools, memory, agent_type, verbose, **kwargs)
        
        # Initialize LangChain agent in constructor
        from langchain.agents import initialize_agent
        self._executor = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=self.agent_type,
            memory=self.memory,
            verbose=self.verbose,
            **self.extra_config
        )

    def query(self, query, prompt=None, context=None):
        if self._executor is None:
            raise RuntimeError("Agent not initialized.")
        input_str = ""
        if prompt:
            input_str += f"{prompt}\n"
        if context:
            input_str += f"{context}\n"
        input_str += str(query)
        return self._executor.run(input_str) 