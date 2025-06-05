from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CreateFolder(BaseModel):
    user_id             : str
    folder_name         : str
    parent_id           : Optional[str] = None
    
class DeleteFolder(BaseModel):
    user_id             : str
    folder_id           : str
    
class ListFolders(BaseModel):
    user_id             : str
    parent_id           : Optional[str] = ""
    folder_id           : Optional[str] = ""
    
class renameFolder(BaseModel):
    user_id             : str
    folder_id           : str
    new_folder_name     : str