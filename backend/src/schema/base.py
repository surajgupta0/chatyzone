from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AUTHPARAMS(BaseModel):
    user_id   : Optional[str] = ""
    email     : Optional[str] = ""
    phone     : Optional[str] = ""