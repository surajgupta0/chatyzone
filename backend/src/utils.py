from .core.database import MongoManager

from typing import Optional, Dict, Any, List, Union
from fastapi.responses import JSONResponse

async def Query(
    collection_name   : str,
    operation         : str,
    query             : Optional[Dict[str, Any]] = None,
    data              : Optional[Dict[str, Any]] = None,
    projection        : Optional[Dict[str, int]] = None,
    sort              : Optional[List[tuple]]    = None
):
    try:
        mongo_manager = MongoManager()

        if operation == "insert_one":
            result = await mongo_manager.insert_one(collection_name, data or {})
        elif operation == "insert_many":
            result = await mongo_manager.insert_many(collection_name, data or [])
        elif operation == "get_one":
            result = await mongo_manager.find_one(collection_name, query or {}, projection, sort or [])
        elif operation == "get_many":
            result = await mongo_manager.find_many(collection_name, query or {}, projection, sort or [])
        elif operation == "update_one":
            result = await mongo_manager.update_one(collection_name, query or {}, data or {})
        elif operation == "update_many":
            result = await mongo_manager.update_many(collection_name, query or {}, data or {})
        elif operation == "delete_one":
            result = await mongo_manager.delete_one(collection_name, query or {})
        elif operation == "delete_many":
            result = await mongo_manager.delete_many(collection_name, query or {})
        else:
            return JSONResponse(
                status_code   = 400,
                content       = {
                    "status"  : 400,
                    "message" : "Invalid operation type",
                    "error"   : "Invalid operation type"
                }
            )

        return result
    
    except Exception as e:
        return JSONResponse(
            status_code         = 500,
            content             = {
                "status"        : "false",
                "message"       : "MongoDB operation error",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno)
            }
        )
        
async def fnMakeId(
    collection_name   : str,
    prefix            : str,
    sort              : str,
):
    try:
        result = await Query(
            collection_name   = collection_name,
            operation         = "get_one",
            sort              = [(sort, -1)]
        )

        if isinstance(result, JSONResponse):
            return result
        
        if not result:
            return f"{prefix}0001"
        
        last_id       = result.get(sort)
        last_id_num   = int(last_id.replace(prefix, ""))
        new_id        = f"{prefix}{str(int(last_id_num+1)).zfill(4)}"
        
        return new_id
    
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={
                "status"    : 500,
                "message"   : "MongoDB connection error",
                "error"     : str(e),
                "error_line" : str(e.__traceback__.tb_lineno),
            }
        )
            
        
        
