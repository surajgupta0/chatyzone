from .base import AUTHPARAMS
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CreateFolder(AUTHPARAMS):
    user_id             : str
    folder_name         : str
    folder_path         : Optional[str] = None