from .base import AUTHPARAMS
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class UploadFile(AUTHPARAMS):
    file_name           : str = "sample.pdf"
    file_path           : str = "/path/to/sample.pdf"
    file_size           : int = 1024
    file_type           : str = "application/pdf"
    uploaded_at         : Optional[str] = None
    uploaded_by         : Optional[str] = None
    status              : Optional[str] = "uploaded"
    tags                : List[str] = []
    
class GetFile(AUTHPARAMS):
    user_id             : str
    directory           : Optional[str] = None
    file_ext            : Optional[str] = None
    file_name           : Optional[str] = None
    file_id             : Optional[str] = None 