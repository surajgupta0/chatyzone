from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from beanie import init_beanie
from typing import Optional, List, Dict, Any
from ..core import variables
from urllib.parse import quote_plus
from .model_mapping import mongoModels

class MongoManager:
    
    def __init__(self):
        try:
            self.mogo_uri   = f"mongodb://{quote_plus(variables.MONGO_USERNAME)}:{quote_plus(variables.MONGO_PASSWORD)}@{variables.MONGO_HOST}:{variables.MONGO_PORT}/{variables.MONGO_DB}?authSource=admin"
            self.client     = AsyncIOMotorClient(self.mogo_uri)
            self.db         = self.client[variables.MONGO_DB]
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB connection error",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )
    
    async def get_db(self):
        try:
            if not self.db:
                self.__init__()  # Reinitialize the connection if not established
            return self.db

        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : 500,
                    "error"         : str(e),
                    "message"       : "MongoDB to get database error",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )
        
    async def get_model(self, model_name: str):
        try:            
            if model_name in mongoModels:
                model = mongoModels[model_name]
                await init_beanie(database=self.db, document_models=[model])
                return model
            
            else:
                return JSONResponse(
                    status_code   = 404,
                    content       = {
                        "status"  : 404,
                        "error"   : "Model not found",
                        "message" : "Model not found"
                    }
                )
        
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "message"       : "MongoDB to get model error",
                    "error"         : str(e),
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__
                }
            )

    async def insert_one(self, model_name: str, data: dict):
        try:
            model = await self.get_model(model_name)
            if isinstance(model, JSONResponse):
                return model
            document = model(**data)
            result = await document.insert()
            return result

        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB fail to insert",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )
    
    async def insert_many(self, model_name: str, data_list: List[dict]):
        try:
            model = await self.get_model(model_name)
            if isinstance(model, JSONResponse):
                return model
            documents = [model(**data) for data in data_list]
            result = await model.insert_many(documents)
            return result
        
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB fail to insert",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__
                }
            )

    async def find_one(self, model_name: str, query: dict, projection: Optional[Dict] = None, sort: Optional[List] = None):
        try:
            model = await self.get_model(model_name)
            if isinstance(model, JSONResponse):
                return model
            result = await model.find(query, sort=sort).limit(1).to_list()
            return result[0].model_dump() if result else {}
        
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB fail to find",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )
    
    async def find_many(self, model_name: str, query: dict, projection: Optional[Dict] = None, sort: Optional[List] = None):
        try:
            model = await self.get_model(model_name)
            if isinstance(model, JSONResponse):
                return model
            result = await model.find(query, sort=sort).to_list()
            return [item.model_dump() for item in result] if result else []
        
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB fail to find",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )
            
    async def update_one(self, model_name: str, query: dict, data: dict):
        try:
            model = await self.get_model(model_name)
            if isinstance(model, JSONResponse):
                return model
            result = await model.find(query).update({"$set": data})
            print(result)
            
            return result.raw_result if result else {}
        
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB fail to update",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )
            
    async def update_many(self, model_name: str, query: dict, data: dict):
        try:
            model = await self.get_model(model_name)
            if isinstance(model, JSONResponse):
                return model
            result = await model.update_many(query, {"$set": data})
            return result.raw_result
        
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB fail to update",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )
            
    async def delete_one(self, model_name: str, query: dict):
        try:
            model = await self.get_model(model_name)
            if isinstance(model, JSONResponse):
                return model
            result = await model.delete_one(query)
            return result
        
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB fail to delete",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )
            
    async def delete_many(self, model_name: str, query: dict):
        try:
            model = await self.get_model(model_name)
            if isinstance(model, JSONResponse):
                return model
            result = await model.delete_many(query)
            return result
        
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB fail to delete",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )
    
    async def close(self):
        try:
            self.client.close()
        except Exception as e:
            return JSONResponse(
                status_code         = 500,
                content             = {
                    "status"        : "false",
                    "error"         : str(e),
                    "message"       : "MongoDB fail to close connection",
                    "error_line"    : str(e.__traceback__.tb_lineno),
                    "page"          : __name__,
                }
            )