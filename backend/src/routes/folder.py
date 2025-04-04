from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..schema import folder
from typing import Optional, List
from ..utils import Query, fnMakeId
from datetime import datetime
import os
from ..core import variables
    
router = APIRouter(prefix="/folder", tags=["Folder"])

def create_user_folder(user_id: str, folder_name: str = None, folder_path: str = None):
    user_folder = os.path.join(variables.BASE_UPLOAD_DIR, user_id)
    
    if folder_path:
        user_folder = os.path.join(user_folder, folder_path)
    
    if folder_name:
        user_folder = os.path.join(user_folder, folder_name)
    
    os.makedirs(user_folder, exist_ok = True)
    
    return user_folder

# Upload Files
@router.post("/folder/create", status_code = 202)
async def create_folder(
    schema: folder.CreateFolder, 
):
    try:
        folder_path = os.path.join(variables.BASE_UPLOAD_DIR, schema.user_id, schema.folder_path, schema.folder_name)

        if os.path.exists(folder_path):
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"    : 'false',
                    "message"   : "Folder already exists",
                    "error"     : "Folder already exists",
                }
            )
            
        folder_path = create_user_folder(schema.user_id, schema.folder_name, schema.folder_path)
        
        return JSONResponse(
            status_code   = status.HTTP_201_CREATED,
            content       = {
                "status"    : 'true',
                "message"   : "Folder created successfully",
                "data"      : {
                    "folder_path" : folder_path,
                }
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content       = {
                "status"        : 'false',
                "message"       : "Internal server error",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno),
            }
        )
        
@router.get("/folder/list", status_code = 200)
async def list_folders(
    user_id: str,
):
    try:
        user_folder = os.path.join(variables.BASE_UPLOAD_DIR, user_id)
        arrFolders = [[f for f in os.listdir(user_folder) if os.path.isdir(os.path.join(user_folder, f))]]
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "Folder list retrieved successfully",
                "data"      : arrFolders
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content       = {
                "status"        : 'false',
                "message"       : "Internal server error",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno),
            }
        )
        
@router.delete("/delete", status_code=200)
async def delete_folder(user_id: str, folder_name: str, folder_path:Optional['str']=''):
    try:
        folder_path = os.path.join(variables.BASE_UPLOAD_DIR, user_id, folder_path, folder_name)
        
        if not os.path.exists(folder_path):
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"    : 'false',
                    "message"   : "Folder does not exist",
                    "error"     : "Folder does not exist",
                }
            )
        
        os.rmdir(folder_path)
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "Folder deleted successfully",
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content       = {
                "status"        : 'false',
                "message"       : "Internal server error",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno),
            }
        )
        
@router.post("/rename", status_code=200)
async def rename_folder(user_id: str, folder_name: str, new_folder_name: str, folder_path:Optional['str']=''):
    try:
        folder_path = os.path.join(variables.BASE_UPLOAD_DIR, user_id, folder_path, folder_name)
        new_folder_path = os.path.join(variables.BASE_UPLOAD_DIR, user_id, folder_path, new_folder_name)
        
        if not os.path.exists(folder_path):
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"    : 'false',
                    "message"   : "Folder does not exist",
                    "error"     : "Folder does not exist",
                }
            )
        
        os.rename(folder_path, new_folder_path)
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "Folder renamed successfully",
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content       = {
                "status"        : 'false',
                "message"       : "Internal server error",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno),
            }
        )