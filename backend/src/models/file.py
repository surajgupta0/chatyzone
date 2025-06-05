from beanie import Document
from typing import Optional, List

class FILE(Document):
    file_id          : str
    created_by       : str
    folder_id        : str
    file_name        : Optional[str] = ''
    file_ext         : Optional[str] = ''
    file_path        : Optional[str] = ''
    file_size        : Optional[int] = 0
    created_at       : Optional[str] = None

    class Config:
        collection = "coll_files"
        allow_null = True