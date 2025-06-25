from ..base_agent import BaseAgent
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import re

class SimpleLLMAgent(BaseAgent):
    """Simple LLM agent that directly generates DSL code without ReAct complexity."""
    
    def __init__(self, llm, tools=None, memory=None, agent_type=None, verbose=True, **kwargs):
        super().__init__(llm, tools, memory, agent_type, verbose, **kwargs)
        
        # Create a simple prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["prompt", "context", "query"],
            template="""
{prompt}

## Examples from Training Data
{context}

## User Request
{query}

## Response Format
Generate ONLY the DSL code block. Do not include any explanations or additional text.

```dsl
RULE [descriptive_rule_name]
WHEN [condition_using_exact_variable_names_from_examples]
THEN [action_using_exact_syntax_from_examples]
[additional WHEN/THEN clauses if needed]
END
```
"""
        )
        
        # Create modern RunnableSequence (replaces deprecated LLMChain)
        self._chain = self.prompt_template | self.llm

    def _extract_dsl_code(self, text):
        """Extract DSL code from LLM response."""
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
        
        return text.strip()

    def _format_examples(self, examples):
        """Format examples for better LLM understanding."""
        if not examples:
            return "No examples available."
        
        formatted_examples = []
        for i, example in enumerate(examples, 1):
            if isinstance(example, dict):
                prompt = example.get('prompt', '')
                dsl_pattern = example.get('dsl_pattern', '')
                if prompt and dsl_pattern:
                    formatted_examples.append(f"Example {i}:")
                    formatted_examples.append(f"Prompt: {prompt}")
                    formatted_examples.append(f"DSL Pattern:")
                    formatted_examples.append(dsl_pattern)
                    formatted_examples.append("")
        
        return "\n".join(formatted_examples)

    def query(self, query, prompt=None, context=None):
        if self._chain is None:
            raise RuntimeError("Agent not initialized.")
        
        # Format context as string with examples
        context_str = self._format_examples(context)
        
        try:
            # Single LLM call - no retries needed
            result = self._chain.invoke({
                "prompt": prompt or "You are a helpful AI assistant that generates DSL code.",
                "context": context_str,
                "query": query
            })
            
            # Extract and return DSL code
            dsl_code = self._extract_dsl_code(result.content)
            return dsl_code
            
        except Exception as e:
            return f"[Error] {str(e)}" 