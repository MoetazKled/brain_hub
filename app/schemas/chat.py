from pydantic import BaseModel
from datetime import datetime
from typing import Optional , List

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    use_rag: bool = True

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    message_id: str
    timestamp: datetime
    sources: Optional[List[str]] = None