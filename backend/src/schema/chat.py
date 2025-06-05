from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class chat(BaseModel):
    user_id           : Optional[str] = None
    reference_id       : Optional[str] = None
    reference_type     : Optional[str] = None
    message           : Optional[str] = None
    
class GetChat(BaseModel):
    chat_id             : Optional[str] = None
    user_id             : Optional[str] = None
    reference_id         : Optional[str] = None
    reference_type       : Optional[str] = None
    
class GetChatHistory(BaseModel):
    user_id             : Optional[str] = None
    chat_id             : Optional[str] = None
    reference_id        : Optional[str] = None
    reference_type      : Optional[str] = None