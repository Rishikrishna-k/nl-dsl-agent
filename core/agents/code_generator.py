from typing import Optional
import logging

from .base_agent import BaseAgent
from ..models.agent import AgentConfig, AgentResponse, AgentContext


class ExampleService:
    """Placeholder for example service"""
    async def get_relevant_examples(self, language: str, message: str):
        return []


class GrammarService:
    """Placeholder for grammar service"""
    async def get_grammar(self, language: str):
        return None


class CodeGeneratorAgent(BaseAgent):
    """Agent responsible for generating code based on user prompts"""
    
    def __init__(self, config: AgentConfig, example_service: ExampleService, grammar_service: GrammarService):
        super().__init__(config)
        self.example_service = example_service
        self.grammar_service = grammar_service
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def execute(self, context: AgentContext) -> AgentResponse:
        """Generate code based on the user's prompt"""
        try:
            # Get relevant examples
            examples = await self.example_service.get_relevant_examples(
                context.language, 
                context.user_message
            )
            
            # Get grammar if available
            grammar = await self.grammar_service.get_grammar(context.language)
            
            # Build enhanced context
            enhanced_context = AgentContext(
                session_id=context.session_id,
                language=context.language,
                user_message=context.user_message,
                chat_history=context.chat_history,
                examples=examples,
                grammar=grammar,
                max_iterations=context.max_iterations
            )
            
            # Build the prompt
            prompt = self._build_prompt(enhanced_context)
            
            # TODO: Call OpenAI API here
            # For now, return a placeholder response
            generated_code = self._generate_placeholder_code(context.language, context.user_message)
            
            return AgentResponse(
                agent_name=self.config.name,
                content=generated_code,
                success=True,
                error_message=None,
                processing_time=None,
                tokens_used=None
            )
            
        except Exception as e:
            self.logger.error(f"Error generating code: {str(e)}")
            return AgentResponse(
                agent_name=self.config.name,
                content="",
                success=False,
                error_message=str(e),
                processing_time=None,
                tokens_used=None
            )
    
    def _generate_placeholder_code(self, language: str, prompt: str) -> str:
        """Generate placeholder code for demonstration"""
        if "classroom" in language.lower():
            return f"""// Generated code for: {prompt}
program ClassroomProgram {{
    action main {{
        // TODO: Implement based on prompt
        Notes.take("Hello from Classroom DSL!");
    }}
}}"""
        elif "csharp" in language.lower():
            return f"""// Generated code for: {prompt}
using System;

public class GeneratedClass
{{
    public static void Main()
    {{
        Console.WriteLine("Hello from C#!");
        // TODO: Implement based on prompt
    }}
}}"""
        else:
            return f"// Generated code for {language}: {prompt}\n// TODO: Implement actual code generation"
    
    def _build_prompt(self, context: AgentContext) -> str:
        """Build a comprehensive prompt for code generation"""
        prompt = super()._build_prompt(context)
        
        # Add specific instructions for code generation
        prompt += "\n\nInstructions:\n"
        prompt += "1. Generate only the code, no explanations\n"
        prompt += "2. Follow the language syntax and conventions\n"
        prompt += "3. Use the provided examples as reference\n"
        prompt += "4. Ensure the code is complete and executable\n"
        
        return prompt 