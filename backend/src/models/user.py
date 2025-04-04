from beanie import Document
from typing import Optional, List

class USER(Document):
    user_id       : Optional[str] = ''
    first_name    : Optional[str] = ''
    last_name     : Optional[str] = ''
    email         : str
    password      : str
    phone         : Optional[str] = ''
    is_active     : Optional[str] = 'Y'
    role          : Optional[str] = 'user'
    created_at    : Optional[str] = None
    updated_at    : Optional[str] = None
    last_login    : Optional[str] = None
    
    class Config:
        collection = "coll_users"
        allow_null = True
    
    