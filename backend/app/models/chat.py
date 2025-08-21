from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = datetime.now()

class ChatRequest(BaseModel):
    message: str
    website_id: str
    conversation_id: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None

class Conversation(BaseModel):
    id: str
    website_id: str
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

class ConversationWithMessages(Conversation):
    messages: List[ChatMessage] = [] 