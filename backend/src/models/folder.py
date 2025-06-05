from beanie import Document
from typing import Optional, List

class FOLDER(Document):
    
    folder_id        : Optional[str] = ''
    folder_name     : Optional[str] = ''
    folder_path     : Optional[str] = ''
    parent_id       : Optional[str] = ''
    created_at      : Optional[str] = None
    updated_at      : Optional[str] = None
    created_by      : Optional[str] = None

    class Config:
        collection = "coll_folders"
        allow_null = True