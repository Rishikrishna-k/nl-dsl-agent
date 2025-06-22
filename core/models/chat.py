from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    role: MessageRole = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")
    session_id: Optional[str] = Field(None, description="Chat session ID")


class ChatSession(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    messages: List[ChatMessage] = Field(default_factory=list, description="Chat messages")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session creation time")
    last_activity: datetime = Field(default_factory=datetime.utcnow, description="Last activity time")
    language: Optional[str] = Field(None, description="Selected language for this session")
    
    def add_message(self, role: MessageRole, content: str) -> None:
        """Add a new message to the session"""
        message = ChatMessage(
            role=role,
            content=content,
            session_id=self.session_id
        )
        self.messages.append(message)
        self.last_activity = datetime.utcnow()
    
    def get_messages_for_context(self, max_messages: int = 10) -> List[ChatMessage]:
        """Get recent messages for context, prioritizing system messages"""
        if len(self.messages) <= max_messages:
            return self.messages
        
        # Always include system messages
        system_messages = [msg for msg in self.messages if msg.role == MessageRole.SYSTEM]
        other_messages = [msg for msg in self.messages if msg.role != MessageRole.SYSTEM]
        
        # Take the most recent non-system messages
        recent_messages = other_messages[-max_messages + len(system_messages):]
        
        return system_messages + recent_messages 