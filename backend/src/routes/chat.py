from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..schema import chat as chatschema
from ..utils import Query, fnMakeId
from ..core.security import hash_password, verify_password, create_access_token, decode_token, oauth2_scheme
from datetime import datetime
from ..core import variables
import os
from ..ai_models.rag import GenerateResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/chat", status_code = status.HTTP_200_OK)
async def chat(schema: chatschema.chat):
    try:
        user_id       = schema.user_id
        reference_id   = schema.reference_id
        reference_type = schema.reference_type
        query         = schema.message

        # Step 1: Get file(s)
        file_query = {
            "created_by"           : user_id,
        }
        
        if reference_type == 'folder':
            file_query["folder_id"] = reference_id
        elif reference_type == 'file':
            file_query["file_id"] = reference_id
        else:
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"  : False,
                    "message" : "Invalid reference type."
                }
            )

        # return file_query
        arrFiles = await Query(
            collection_name   = 'coll_files',
            operation         = "get_many",
            query             = file_query
        )

        if isinstance(arrFiles, JSONResponse):
            return arrFiles
        
        if not arrFiles:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "No files found."
                }
            )

        existing_chat = await Query(
            collection_name   = 'coll_chat',
            operation         = "get_one",
            query             = {
                "created_by"    : user_id,
                "reference_id"   : reference_id
            }
        )
        
        if isinstance(existing_chat, JSONResponse):
            return existing_chat
        
        if not existing_chat:
            
            chat_id = await fnMakeId(
                collection_name   = 'coll_chat',
                prefix            = 'CHAT',
                sort              = 'chat_id'
            )
            
            if isinstance(chat_id, JSONResponse):
                return chat_id


            # Create a new chat
            chat_data = {
                "chat_id"         : chat_id,
                "chat_history"    : [],
                "reference_id"     : reference_id,
                "reference_type"   : reference_type,
                "created_at"      : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at"      : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "created_by"      : user_id
            }

            insert_result = await Query(
                collection_name   = 'coll_chat',
                operation         = 'insert_one',
                data              = chat_data
            )

            if isinstance(insert_result, JSONResponse):
                return insert_result

            chat_history = []
        else:
            chat_id = existing_chat.get('chat_id')
            chat_history = existing_chat.get('chat_history', [])

        # Step 3: Generate response using LLM or internal logic
        file_paths = [f['file_path'] for f in arrFiles]

        generated_response = await GenerateResponse(
            query         = query,
            files_path    = file_paths,
            chat_history  = chat_history
        )

        if isinstance(generated_response, JSONResponse):
            return generated_response

        # Step 4: Append to chat history
        chat_history.append({
            "query"       : query,
            "response"    : generated_response,
            "created_at"  : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        update_result = await Query(
            collection_name       = 'coll_chat',
            operation             = 'update_one',
            query                 = {"created_by": user_id, "chat_id": chat_id},
            data                  ={
                "chat_history"    : chat_history,
                "updated_at"      : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

        if isinstance(update_result, JSONResponse):
            return update_result

        return JSONResponse(
            status_code               = status.HTTP_200_OK,
            content                     = {
                "status"              : True,
                "message"             : "Chat history updated successfully.",
                "data": {
                    "chat_id"         : chat_id,
                    "chat_history"    : chat_history
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code         = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content             = {
                "status"        : False,
                "message"       : "Internal server error.",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno)
            }
        )

@router.post("/get", status_code=status.HTTP_200_OK)
async def get_chats(schema: chatschema.GetChat):
    try:
        user_id       = schema.user_id
        reference_id   = schema.reference_id
        chat_id       = schema.chat_id

        # Step 1: Fetch chats based on folder path and user ID
        query = {
            "created_by"       : user_id,
        }
        
        if reference_id:
            query["reference_id"] = reference_id
            
        if chat_id:
            query["chat_id"] = chat_id
            
        chats = await Query(
            collection_name   = 'coll_chat',
            operation         = "get_one",
            query             = query
        )

        if isinstance(chats, JSONResponse):
            return chats
        
        if not chats:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "No chats found."
                }
            )

        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"  : True,
                "message" : "Chats fetched successfully.",
                "data"    : chats.get('chat_history')
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content       = {
                "status"    : False,
                "message"   : "Internal server error.",
                "error"     : str(e),
                "error_line": str(e.__traceback__.tb_lineno)
            }
        )

@router.post("/history", status_code=status.HTTP_200_OK)
async def get_chat_history(schema: chatschema.GetChatHistory):
    try:
        user_id           = schema.user_id
        chat_id           = schema.chat_id
        reference_type    = schema.reference_type
        reference_id      = schema.reference_id

        # Step 1: Fetch chat history based on chat ID and user ID
        query = {
            "created_by"   : user_id,
        }
        
        if chat_id:
            query["chat_id"] = chat_id
        
        if reference_id:
            query["reference_id"] = reference_id
            
        
        chat_history = await Query(
            collection_name   = 'coll_chat',
            operation         = "get_one",
            query             = query
        )

        if isinstance(chat_history, JSONResponse):
            return chat_history
        
        if not chat_history:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "No chat history found."
                }
            )

        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"  : True,
                "message" : "Chat history fetched successfully.",
                "data"    : chat_history.get('chat_history', [])
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content       = {
                "status"    : False,
                "message"   : "Internal server error.",
                "error"     : str(e),
                "error_line": str(e.__traceback__.tb_lineno)
            }
        )