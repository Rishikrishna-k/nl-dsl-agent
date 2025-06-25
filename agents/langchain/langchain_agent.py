from ..base_agent import BaseAgent
import re

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
            handle_parsing_errors=True,
            max_iterations=3,  # Limit retries to prevent infinite loops
            **self.extra_config
        )

    def _extract_dsl_code(self, text):
        """Extract DSL code from LLM output using regex."""
        # Look for DSL code blocks
        dsl_pattern = r'```dsl\s*\n(.*?)\n```'
        matches = re.findall(dsl_pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        # Look for RULE patterns without code blocks
        rule_pattern = r'RULE\s+\w+.*?END'
        matches = re.findall(rule_pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        return None

    def query(self, query, prompt=None, context=None):
        if self._executor is None:
            raise RuntimeError("Agent not initialized.")
        input_str = ""
        if prompt:
            input_str += f"{prompt}\n"
        if context:
            input_str += f"{context}\n"
        input_str += str(query)
        
        try:
            return self._executor.run(input_str)
        except Exception as e:
            # Try to extract DSL code from the error message
            error_str = str(e)
            dsl_code = self._extract_dsl_code(error_str)
            
            if dsl_code:
                return f"Generated DSL Code:\n{dsl_code}"
            else:
                # If no DSL code found, return a helpful error message
                return f"[Agent Error] Could not parse LLM output. Error: {str(e)[:200]}..." 