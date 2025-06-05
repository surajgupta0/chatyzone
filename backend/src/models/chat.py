from beanie import Document
from typing import Optional, List, Dict

class CHAT(Document):
    chat_id         : Optional[str] = ""
    reference_id     : Optional[str] = ""
    reference_type   : Optional[str] = ""
    chat_history    : Optional[List[Dict]] = []
    created_at      : Optional[str] = ""
    updated_at      : Optional[str] = ""
    created_by      : Optional[str] = ""
    
    class Settings:
        collection = "coll_chat"
    
    
    