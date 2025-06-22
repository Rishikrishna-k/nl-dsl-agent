from typing import Optional, List
import logging
import re

from .base_agent import BaseAgent
from ..models.agent import AgentConfig, AgentResponse, AgentContext


class CodeValidatorAgent(BaseAgent):
    """Agent responsible for validating generated code using grammar parsers"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def execute(self, context: AgentContext) -> AgentResponse:
        """Validate the generated code"""
        try:
            # Extract code from the last assistant message
            code = self._extract_code_from_context(context)
            
            if not code:
                return AgentResponse(
                    agent_name=self.config.name,
                    content="No code found to validate",
                    success=False,
                    error_message="No code found in context",
                    processing_time=None,
                    tokens_used=None
                )
            
            # Validate the code
            validation_result = await self._validate_code(code, context.language)
            
            if validation_result["is_valid"]:
                return AgentResponse(
                    agent_name=self.config.name,
                    content="::success::",
                    success=True,
                    error_message=None,
                    processing_time=None,
                    tokens_used=None
                )
            else:
                return AgentResponse(
                    agent_name=self.config.name,
                    content=f"Validation failed: {validation_result['errors']}",
                    success=False,
                    error_message=validation_result["errors"],
                    processing_time=None,
                    tokens_used=None
                )
                
        except Exception as e:
            self.logger.error(f"Error validating code: {str(e)}")
            return AgentResponse(
                agent_name=self.config.name,
                content="",
                success=False,
                error_message=str(e),
                processing_time=None,
                tokens_used=None
            )
    
    def _extract_code_from_context(self, context: AgentContext) -> Optional[str]:
        """Extract code from the chat context"""
        # Look for code in the last assistant message
        for message in reversed(context.chat_history):
            if message.get("role") == "assistant":
                content = message.get("content", "")
                # Simple code extraction - look for code blocks
                code_match = re.search(r'```(?:\w+)?\n(.*?)\n```', content, re.DOTALL)
                if code_match:
                    return code_match.group(1).strip()
                # If no code block, return the entire content
                return content.strip()
        return None
    
    async def _validate_code(self, code: str, language: str) -> dict:
        """Validate code using language-specific rules"""
        errors = []
        
        if "classroom" in language.lower():
            errors = self._validate_classroom_code(code)
        elif "csharp" in language.lower():
            errors = self._validate_csharp_code(code)
        else:
            # Generic validation
            errors = self._validate_generic_code(code)
        
        return {
            "is_valid": len(errors) == 0,
            "errors": "; ".join(errors) if errors else None
        }
    
    def _validate_classroom_code(self, code: str) -> List[str]:
        """Validate Classroom DSL code"""
        errors = []
        
        # Check for required program structure
        if "program" not in code:
            errors.append("Missing 'program' declaration")
        
        if "action main" not in code:
            errors.append("Missing 'action main'")
        
        # Check for basic syntax
        if code.count("{") != code.count("}"):
            errors.append("Mismatched braces")
        
        if code.count("(") != code.count(")"):
            errors.append("Mismatched parentheses")
        
        return errors
    
    def _validate_csharp_code(self, code: str) -> List[str]:
        """Validate C# code"""
        errors = []
        
        # Check for basic C# syntax
        if "using" not in code and "namespace" not in code:
            errors.append("Missing using statements or namespace")
        
        if "class" not in code:
            errors.append("Missing class declaration")
        
        if code.count("{") != code.count("}"):
            errors.append("Mismatched braces")
        
        if code.count("(") != code.count(")"):
            errors.append("Mismatched parentheses")
        
        return errors
    
    def _validate_generic_code(self, code: str) -> List[str]:
        """Generic code validation"""
        errors = []
        
        # Basic syntax checks
        if code.count("{") != code.count("}"):
            errors.append("Mismatched braces")
        
        if code.count("(") != code.count(")"):
            errors.append("Mismatched parentheses")
        
        if code.count("[") != code.count("]"):
            errors.append("Mismatched brackets")
        
        return errors
    
    def _build_prompt(self, context: AgentContext) -> str:
        """Build a comprehensive prompt for code validation"""
        prompt = super()._build_prompt(context)
        
        # Add specific instructions for validation
        prompt += "\n\nValidation Instructions:\n"
        prompt += "1. Check syntax and grammar compliance\n"
        prompt += "2. Verify code structure and completeness\n"
        prompt += "3. Report specific errors with line numbers if possible\n"
        prompt += "4. Respond with '::success::' if code is valid\n"
        
        return prompt 