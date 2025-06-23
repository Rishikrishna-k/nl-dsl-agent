class BaseAgent:
    """Abstract base class for all agents with common functionality."""
    def __init__(self, llm, tools=None, memory=None, agent_type=None, verbose=True, **kwargs):
        self.llm = llm
        self.tools = tools or []
        self.memory = memory
        self.agent_type = agent_type
        self.verbose = verbose
        self.extra_config = kwargs
        self._executor = None  # To be set by subclass

    def query(self, query, prompt=None, context=None):
        """Send a query to the agent."""
        if self._executor is None:
            raise RuntimeError("Agent not initialized.")
        raise NotImplementedError 