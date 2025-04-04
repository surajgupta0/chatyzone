from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AdUpdateUser(BaseModel):
    user_id             : Optional[str] = ""
    first_name          : Optional[str] = "Suraj"
    last_name           : Optional[str] = "Gupta"
    email               : str = "suraj@gmail.com"
    password            : str = "suraj123"
    confirm_password    : str = "suraj123"
    profile_picture     : Optional[str] = "abc"
    phone               : Optional[str] = "9876543210"
    role                : Optional[str] = "user"
    is_active           : Optional[str] = 'Y'

    class Config:
        orm_mode = True
        
class LoginUser(BaseModel):
    email       : Optional[str] = ""
    phone       : Optional[str] = ""
    user_id     : Optional[str] = ""
    password    : str
    
    
class GetProfile(BaseModel):
    user_id     : Optional[str] = ""
    email       : Optional[str] = ""
    phone       : Optional[str] = ""