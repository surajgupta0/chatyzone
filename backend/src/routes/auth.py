from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..schema import user
from ..utils import Query, fnMakeId
from ..core.security import hash_password, verify_password, create_access_token, decode_token, oauth2_scheme
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

#User Registration
@router.post("/register", status_code = 201)
async def register_user(schema: user.AdUpdateUser):
    try:
        
        if schema.password != schema.confirm_password:
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {"message": "Passwords do not match"}
            )
        
        user_id = schema.user_id or await fnMakeId(
            collection_name='coll_users', prefix='USR', sort='user_id'
        )
        

        if isinstance(user_id, JSONResponse):
            return user_id

        data = {
            "user_id"       : user_id,
            "email"         : schema.email,
            "password"      : hash_password(schema.password),
            "phone"         : schema.phone,
            "first_name"    : schema.first_name,
            "last_name"     : schema.last_name,
            "role"          : schema.role,
            "is_active"     : schema.is_active,
            "updated_at"    : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        existing_user = await Query(
            collection_name   = 'coll_users',
            operation         = 'get_one',
            query             = {'user_id':user_id},
        )
        
        duplicate_user = await Query(
            collection_name   = 'coll_users',
            operation         = 'get_one',
            query             = {
                '$or': [
                    {'email'  : schema.email},
                    {'phone'  : schema.phone}
                ]
            },  
        )
        
        if isinstance(existing_user, JSONResponse) or isinstance(duplicate_user, JSONResponse):
            return existing_user if existing_user else duplicate_user

        
        if existing_user:
            if duplicate_user.get('user_id') != user_id:
                return JSONResponse(
                    status_code   = status.HTTP_400_BAD_REQUEST,
                    content       = {
                        "status"    : 'false',
                        "message"   : "Mobile number or email already exists",
                        "error"     : "Mobile number or email already exists"
                    }
                )
            
            update_user = await Query(
                collection_name   = 'coll_users',
                operation         = 'update_one',
                query             = {'user_id': user_id},
                data              = data,
            )
            
            if isinstance(update_user, JSONResponse):
                return update_user
            
            return JSONResponse(
                status_code   = status.HTTP_200_OK,
                content       = {
                    "status"    : 'true',
                    "message"   : "User updated successfully",
                    "data"      : update_user
                }
            )
        
        if duplicate_user:
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"    : 'false',
                    "message"   : "Mobile number or email already exists",
                    "error"     : "Mobile number or email already exists"
                }
            )
        
        data['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        
        user = await Query(
            collection_name   = 'coll_users',
            operation         = 'insert_one',
            data              = data,
        )
        
        if isinstance(user, JSONResponse):
            return user
        
        return JSONResponse(
            status_code   = status.HTTP_201_CREATED,
            content       = {
                "status"    : 'true',
                "message"   : "User registered successfully",
                "data"      : user
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

#User Login
@router.post("/login", status_code = 200)
async def login_user(schema: user.LoginUser):
    try:
        if not schema.email and not schema.phone and not schema.user_id:
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"    : 'false',
                    "message"   : "Email or phone or user_id is required",
                    "error"     : "Email or phone or user_id is required"
                }
            )
        
        query = {}
        if schema.email:
            query['email'] = schema.email
        if schema.phone:
            query['phone'] = schema.phone
        if schema.user_id:
            query['user_id'] = schema.user_id
             
        user = await Query(
            collection_name   = 'coll_users',
            operation         = 'get_one',
            query             = query,
        )
        
        if isinstance(user, JSONResponse):
            return user
        
        if not user:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"    : 'false',
                    "message"   : "User not found",
                    "error"     : "User not found"
                }
            )
        
        if not verify_password(schema.password, user.get('password')):
            return JSONResponse(
                status_code   = status.HTTP_401_UNAUTHORIZED,
                content       = {
                    "status"    : 'false',
                    "message"   : "Invalid credentials",
                    "error"     : "Invalid credentials"
                }
            )
        
        arrUpdateUser = await Query(
            collection_name   = 'coll_users',
            operation         = 'update_one',
            query             = {'user_id': user['user_id']},
            data              = {
                'last_login'    : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        
        if isinstance(arrUpdateUser, JSONResponse):
            return arrUpdateUser
        
        access_token = create_access_token(
            data = {
                "sub"   : user['user_id'],
                "role"  : user['role'],
                "email" : user['email']
            })
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "Login successful",
                "data"      : {
                    "access_token"  : access_token,
                    "token_type"    : "bearer",
                    "user_id"       : user['user_id'],
                    "role"          : user['role'],
                    "email"         : user['email'],
                    "phone"         : user['phone'],
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
        
@router.post("/profile/get", status_code = 200)
async def get_user_profile(schema : user.GetProfile):
    try:
        if not schema.user_id:
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"    : 'false',
                    "message"   : "user_id is required",
                    "error"     : "user_id is required"
                }
            )
        
        user = await Query(
            collection_name   = 'coll_users',
            operation         = 'get_one',
            query             = {
                '$or': [
                    {'user_id'  : schema.user_id},
                    {'email'    : schema.email},
                    {'phone'    : schema.phone}
                ]
            },
        )
        
        if isinstance(user, JSONResponse):
            return user
        
        if not user:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"    : 'false',
                    "message"   : "User not found",
                    "error"     : "User not found"
                }
            )
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "User profile fetched successfully",
                "data"      : user
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
        