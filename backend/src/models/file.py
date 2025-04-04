from beanie import Document
from typing import Optional, List

class FILE(Document):
    file_id          : str
    user_id          : str
    file_name        : Optional[str] = ''
    file_ext         : Optional[str] = ''
    directory        : Optional[str] = None
    file_path        : Optional[str] = ''
    file_size        : Optional[int] = 0
    created_at       : Optional[str] = None

    class Config:
        collection = "coll_files"
        allow_null = True