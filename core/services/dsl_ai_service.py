from typing import Optional, List, Dict, Any
import logging
import asyncio

from ..agents.agent_factory import AgentFactory
from ..models.agent import AgentContext, AgentResponse
from ..models.chat import MessageRole
from .chat_service import ChatService


class DslAIService:
    """Main service for orchestrating DSL code generation and validation"""
    
    def __init__(self, chat_service: ChatService, agent_factory: AgentFactory):
        self.chat_service = chat_service
        self.agent_factory = agent_factory
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.max_iterations = 6
    
    async def ask_ai(self, user_message: str, language: str, session_id: str) -> str:
        """Process a user message and generate a response"""
        try:
            # Get or create session
            session = self.chat_service.get_session(session_id)
            if not session:
                session_id = self.chat_service.create_session(language)
                session = self.chat_service.get_session(session_id)
            
            # Get chat history
            chat_history = self.chat_service.get_chat_history_for_context(session_id)
            
            # Create agent context
            context = AgentContext(
                session_id=session_id,
                language=language,
                user_message=user_message,
                chat_history=chat_history,
                examples=None,
                grammar=None,
                max_iterations=self.max_iterations
            )
            
            # Run the multi-agent system
            response = await self._run_agent_chat(context)
            
            # Add messages to chat history
            self.chat_service.add_message(session_id, MessageRole.USER, user_message)
            self.chat_service.add_message(session_id, MessageRole.ASSISTANT, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing AI request: {str(e)}")
            return f"Error: {str(e)}"
    
    async def _run_agent_chat(self, context: AgentContext) -> str:
        """Run the multi-agent chat system with code generation and validation"""
        code_gen_agent = self.agent_factory.create_code_generator()
        validator_agent = self.agent_factory.create_code_validator()
        
        iteration = 0
        last_code_response = ""
        
        while iteration < self.max_iterations:
            iteration += 1
            self.logger.info(f"Agent iteration {iteration}/{self.max_iterations}")
            
            # Generate code
            code_response = await code_gen_agent.run(context)
            if not code_response.success:
                return f"Code generation failed: {code_response.error_message}"
            
            last_code_response = code_response.content
            
            # Update context with generated code
            context.chat_history.append({
                "role": "assistant",
                "content": code_response.content
            })
            
            # Validate code
            validation_response = await validator_agent.run(context)
            
            if validation_response.success and "::success::" in validation_response.content:
                # Code is valid, return it
                self.logger.info(f"Code validation successful after {iteration} iterations")
                return last_code_response
            
            # Code is invalid, add validation feedback to context
            if validation_response.content:
                context.chat_history.append({
                    "role": "system",
                    "content": f"Validation feedback: {validation_response.content}"
                })
            
            # If we've reached max iterations, return the last generated code
            if iteration >= self.max_iterations:
                self.logger.warning(f"Reached max iterations ({self.max_iterations}), returning last generated code")
                return last_code_response
        
        return last_code_response
    
    async def get_available_languages(self) -> List[str]:
        """Get list of available programming languages"""
        # This would typically come from a configuration or database
        return ["classroom", "csharp", "python", "javascript"]
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a chat session"""
        session = self.chat_service.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session.session_id,
            "language": session.language,
            "message_count": len(session.messages),
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat()
        } 