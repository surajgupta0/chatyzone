from .base import AUTHPARAMS
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class chat(AUTHPARAMS):
    chat_id             : Optional[str] = None
    user_id             : Optional[str] = None
    query               : str = ""
    file_id             : Optional[str] = None
    filde_path          : Optional[str] = None
    file_name           : Optional[str] = None
    
    