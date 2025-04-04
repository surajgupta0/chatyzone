from beanie import Document
from typing import Optional, List, Dict

class CHAT(Document):
    chat_id         : Optional[str] = ""
    chat_type       : Optional[str] = ""
    file_id         : Optional[str] = ""
    file_path       : Optional[str] = ""
    file_name       : Optional[str] = ""
    file_type       : Optional[str] = ""
    chat_history    : Optional[List[Dict]] = []
    created_at      : Optional[Dict] = ""
    updated_at      : Optional[Dict] = ""
    created_by      : Optional[Dict] = ""
    
    class Settings:
        collection = "coll_chat"
    
    
    