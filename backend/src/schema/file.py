from pydantic import BaseModel
from typing import Optional
class GetFile(BaseModel):
    user_id             : str
    file_id             : Optional[str] = None 
    
class RenameFile(BaseModel):
    user_id             : str
    file_id             : str
    new_file_name        : str
    