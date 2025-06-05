from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..schema import folder
from typing import Optional, List
import shutil
from ..utils import Query, fnMakeId
from datetime import datetime
import os
from ..core import variables
import json
    
router = APIRouter(prefix="/folder", tags=["Folder"])

# Upload Files
@router.post("/create", status_code = 202)
async def create_folder(
    schema: folder.CreateFolder,
):
    try:
        user_id       = schema.user_id
        folder_name   = schema.folder_name
        parent_id     = schema.parent_id
        arrParentPath = variables.BASE_UPLOAD_DIR
        
        if parent_id:
            arrParentFolder = await Query(
                collection_name   = 'coll_folders',
                operation         = "get_one",
                query             = {
                    "created_by"    : user_id,
                    "folder_id"     : parent_id
                }
            )
        
            if isinstance(arrParentFolder, JSONResponse):
                return arrParentFolder
        
            if not arrParentFolder:
                return JSONResponse(
                    status_code   = status.HTTP_404_NOT_FOUND,
                    content       = {
                        "status"  : False,
                        "message" : "Parent folder not found."
                    }
                )
            arrParentPath = arrParentFolder.get('folder_path')
        
        folder_path = os.path.join(arrParentPath, folder_name)
        
        if os.path.exists(folder_path):
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"    : 'false',
                    "message"   : "Folder already exists",
                    "error"     : "Folder already exists",
                }
            )
        
        # Generate a unique file ID
        folder_id = await fnMakeId(
            collection_name   = 'coll_folders',
            prefix            = 'FLDR',
            sort              = 'folder_id'
        )
        
        if isinstance(folder_id, JSONResponse):
            return folder_id

        folder_data = {
            "folder_id"      : folder_id,
            "created_by"     : user_id,
            "folder_name"    : folder_name,
            "folder_path"    : folder_path,
            "parent_id"      : parent_id,
            "created_at"     : datetime.now().isoformat(),
            "updated_at"     : datetime.now().isoformat(),
        }
        
        # Insert folder data into the database
        insert_result = await Query(
            collection_name   = 'coll_folders',
            operation         = "insert_one",
            data              = folder_data
        )
        
        if isinstance(insert_result, JSONResponse):
            return insert_result
        
        # Create the folder
        os.makedirs(folder_path, exist_ok = True)
        
        return JSONResponse(
            status_code   = status.HTTP_201_CREATED,
            content       = {
                "status"    : 'true',
                "message"   : "Folder created successfully",
                "data"      : {
                    "folder_id" : folder_id
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
        
@router.post("/list", status_code = 200)
async def list_folders(
    schema:folder.ListFolders
):
    try:
        
        query_filter = {
            "created_by"  : schema.user_id,
        }
        
        if schema.parent_id:
            query_filter["parent_id"] = schema.parent_id
            
        if schema.folder_id:
            query_filter["folder_id"] = schema.folder_id
            
        arrFolders = await Query(
            collection_name   = 'coll_folders',
            operation         = "get_many",
            query             = query_filter
        )
        
        if isinstance(arrFolders, JSONResponse):
            return arrFolders
        
        if not arrFolders:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "No folders found."
                }
            )
            
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"  : True,
                "message" : "Folders retrieved successfully.",
                "data"    : arrFolders
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
        
@router.post("/delete", status_code=200)
async def delete_folder(
    schema:folder.DeleteFolder
    ):
    try:
        folder = await Query(
            collection_name   = 'coll_folders',
            operation         = "get_one",
            query             = {
                "created_by"    : schema.user_id,
                "folder_id"     : schema.folder_id
            }
        )
        
        if isinstance(folder, JSONResponse):
            return folder
        
        if not folder:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "Folder not found."
                }
            )
            
        folder_path = folder.get('folder_path')
        
        # Delete folder from the database
        delete_result = await Query(
            collection_name   = 'coll_folders',
            operation         = "delete_one",
            query             = {
                "created_by"    : schema.user_id,
                "folder_id"     : schema.folder_id
            }
        )
        
        if isinstance(delete_result, JSONResponse):
            return delete_result
        
        shutil.rmtree(folder_path)
        
        rec_delete = await rec_delete_folder(
            user_id         = schema.user_id,
            folder_id       = schema.folder_id
        )
        
        rec_rename_folder_dec = json.loads(rec_delete.body.decode("utf-8"))
        
        if rec_rename_folder_dec.get('status') == 'false':
            return rec_delete
        
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
        
@router.post("/rename", status_code = 200)
async def rename_folder(
    schema: folder.renameFolder
):
    try:
        folder = await Query(
            collection_name   = 'coll_folders',
            operation         = "get_one",
            query             = {
                "created_by"    : schema.user_id,
                "folder_id"     : schema.folder_id
            }
        )
        
        if isinstance(folder, JSONResponse):
            return folder
        
        if not folder:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "Folder not found."
                }
            )
            
        folder_path = folder.get('folder_path')
        
        if not os.path.exists(folder_path):
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"    : 'false',
                    "message"   : "Folder does not exist",
                    "error"     : "Folder does not exist",
                }
            )
        
        updateFolder = await Query(
            collection_name   = 'coll_folders',
            operation         = 'update_one',
            query             = {
                "created_by"  : schema.user_id,
                "folder_id"   : schema.folder_id
            },
            data              = {
                "folder_name" : schema.new_folder_name,
                "folder_path" : os.path.join(os.path.dirname(folder_path), schema.new_folder_name),
                "updated_at"  : datetime.now().isoformat()
            }
        )
        
        if isinstance(updateFolder, JSONResponse):
            return updateFolder
        
        new_path = os.path.join(os.path.dirname(folder_path), schema.new_folder_name)
        
        os.rename(folder_path, new_path)
        
        rec_update = await rec_rename_folder(
            user_id         = schema.user_id,
            folder_id       = schema.folder_id,
            new_folder_path = new_path
        )
        
        rec_update_dec = json.loads(rec_update.body.decode("utf-8"))
        
        if rec_update_dec.get('status') == 'false':
            return rec_update
                
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
        
async def rec_rename_folder(user_id: str, folder_id:str, new_folder_path:str):
    try:
        arrFolders = await Query(
            collection_name   = 'coll_folders',
            operation         = "get_many",
            query             = {
                "created_by"    : user_id,
                "parent_id"     : folder_id
            }
        )
        
        if isinstance(arrFolders, JSONResponse):
            return arrFolders
        
        arrFiles = await Query(
            collection_name   = 'coll_files',
            operation         = "get_many",
            query             = {
                "created_by"    : user_id,
                "folder_id"     : folder_id
            },
        )
        
        if isinstance(arrFiles, JSONResponse):
            return arrFiles
        
        for file in arrFiles:
            file_new_path = os.path.join(new_folder_path, file.get('file_name'))
            
            arrUpdate = await Query(
                collection_name= 'coll_files',
                operation      = 'update_one',
                query          = {
                    "created_by"  : user_id,
                    "file_id"     : file.get('file_id')
                },
                data           = {
                    "file_path"   : file_new_path,
                    "updated_at"  : datetime.now().isoformat()
                }
            )
            
            if isinstance(arrUpdate, JSONResponse):
                return arrUpdate
        
        if not arrFolders:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : 'true',
                    "message" : "No subfolders found."
                }
            )
        
        for folder in arrFolders:
            new_path = os.path.join(new_folder_path, folder.get('folder_name'))
            
            arrUpdate = await Query(
                collection_name= 'coll_folders',
                operation      = 'update_one',
                query          = {
                    "created_by"  : user_id,
                    "folder_id"   : folder.get('folder_id')
                },
                data           = {
                    "folder_path" : new_path,
                    "updated_at"  : datetime.now().isoformat()
                }
            )
            
            res = await rec_rename_folder(
                user_id         = user_id,
                folder_id       = folder.get('folder_id'),
                new_folder_path = new_path
            )
            
            res_dec = json.loads(res.body.decode("utf-8"))
            
            if res_dec.get('status') == 'false':
                return res
            
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "Subfolders renamed successfully",
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
            

async def rec_delete_folder(user_id: str, folder_id:str):
    try:
        arrFolders = await Query(
            collection_name   = 'coll_folders',
            operation         = "get_many",
            query             = {
                "created_by"    : user_id,
                "parent_id"     : folder_id
            }
        )
        
        if isinstance(arrFolders, JSONResponse):
            return arrFolders
        
        arrFiles = await Query(
            collection_name   = 'coll_files',
            operation         = "get_many",
            query             = {
                "created_by"    : user_id,
                "folder_id"     : folder_id
            },
        )
        
        if isinstance(arrFiles, JSONResponse):
            return arrFiles
        
        for file in arrFiles:
            file_path = file.get('file_path')
            
            delete_result = await Query(
                collection_name   = 'coll_files',
                operation         = "delete_one",
                query             = {
                    "created_by"    : user_id,
                    "file_id"       : file.get('file_id')
                }
            )
            
            if isinstance(delete_result, JSONResponse):
                return delete_result
            
            os.remove(file_path)
            
        if not arrFolders:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : 'true',
                    "message" : "No subfolders found."
                }
            )
        
        for folder in arrFolders:
            rec_delete = await rec_delete_folder(
                user_id     = user_id,
                folder_id   = folder.get('folder_id')
            )
            
            rec_delete_dec = json.loads(rec_delete.body.decode("utf-8"))
            
            if rec_delete_dec.get('status') != 'true':
                return rec_delete
        
            delete_result = await Query(
                collection_name   = 'coll_folders',
                operation         = "delete_one",
                query             = {
                    "created_by"    : user_id,
                    "folder_id"     : folder.get('folder_id')
                }
            )
        
            if isinstance(delete_result, JSONResponse):
                return delete_result
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "Subfolders deleted successfully",
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