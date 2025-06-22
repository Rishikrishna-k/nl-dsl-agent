import uuid
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

from ..models.chat import ChatSession, ChatMessage, MessageRole


class ChatService:
    """Service for managing chat sessions and messages"""
    
    def __init__(self, session_timeout: int = 3600):
        self.sessions: Dict[str, ChatSession] = {}
        self.session_timeout = session_timeout
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def create_session(self, language: Optional[str] = None) -> str:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        session = ChatSession(
            session_id=session_id,
            language=language
        )
        
        # Add initial system message
        session.add_message(
            MessageRole.SYSTEM,
            "You are an assistant for generating code that conforms to a given grammar."
        )
        
        self.sessions[session_id] = session
        self.logger.info(f"Created new chat session: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        session = self.sessions.get(session_id)
        if session:
            # Update last activity
            session.last_activity = datetime.utcnow()
        return session
    
    def add_message(self, session_id: str, role: MessageRole, content: str) -> bool:
        """Add a message to a chat session"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.add_message(role, content)
        self.logger.debug(f"Added {role} message to session {session_id}")
        return True
    
    def get_messages(self, session_id: str, max_messages: int = 10) -> List[ChatMessage]:
        """Get messages from a chat session"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        return session.get_messages_for_context(max_messages)
    
    def get_chat_history_for_context(self, session_id: str) -> List[Dict[str, str]]:
        """Get chat history formatted for agent context"""
        messages = self.get_messages(session_id)
        return [
            {
                "role": msg.role.value,
                "content": msg.content
            }
            for msg in messages
        ]
    
    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions and return count of removed sessions"""
        current_time = datetime.utcnow()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if current_time - session.last_activity > timedelta(seconds=self.session_timeout):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
            self.logger.info(f"Removed expired session: {session_id}")
        
        return len(expired_sessions)
    
    def get_session_count(self) -> int:
        """Get the total number of active sessions"""
        return len(self.sessions)
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.logger.info(f"Deleted session: {session_id}")
            return True
        return False 