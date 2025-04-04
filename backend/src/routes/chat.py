from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..schema import chat
from ..utils import Query, fnMakeId
from ..core.security import hash_password, verify_password, create_access_token, decode_token, oauth2_scheme
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/chat", status_code= status.HTTP_200_OK)
async def chat(schema:chat.chat):
    user_id = schema.user_id
    file_name = schema.file_name
    file_path = schema.file_path
    file_type = "folder"
    
    if file_name and file_path:
        arrFile =  await Query(
            collection_name   = 'coll_users',
            operation         = 'get_one',
            query             = {'user_id':user_id},
        )
    
    