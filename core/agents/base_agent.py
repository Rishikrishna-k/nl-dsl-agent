from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import time
import logging

from ..models.agent import AgentConfig, AgentResponse, AgentContext


class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def execute(self, context: AgentContext) -> AgentResponse:
        """Execute the agent's main logic"""
        pass
    
    async def run(self, context: AgentContext) -> AgentResponse:
        """Run the agent with timing and error handling"""
        start_time = time.time()
        
        try:
            self.logger.info(f"Starting {self.config.name} agent")
            response = await self.execute(context)
            response.processing_time = time.time() - start_time
            response.success = True
            self.logger.info(f"Completed {self.config.name} agent in {response.processing_time:.2f}s")
            return response
            
        except Exception as e:
            self.logger.error(f"Error in {self.config.name} agent: {str(e)}")
            return AgentResponse(
                agent_name=self.config.name,
                content="",
                success=False,
                error_message=str(e),
                processing_time=time.time() - start_time,
                tokens_used=None
            )
    
    def _build_prompt(self, context: AgentContext) -> str:
        """Build the prompt for the agent"""
        prompt = f"{self.config.instructions}\n\n"
        
        if context.grammar:
            prompt += f"Grammar:\n{context.grammar}\n\n"
        
        if context.examples:
            prompt += "Examples:\n"
            for example in context.examples:
                prompt += f"Prompt: {example.get('prompt', '')}\n"
                prompt += f"Response: {example.get('response', '')}\n\n"
        
        prompt += f"Language: {context.language}\n"
        prompt += f"User Message: {context.user_message}\n"
        
        return prompt 