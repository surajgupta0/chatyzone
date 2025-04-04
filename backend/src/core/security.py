from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from .variables import * 
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key for signing JWT (use a secure key)
SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM 
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES 

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 1. Hash Password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#  2. Verify Password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 3. Create Access Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode   = data.copy()
    expire      = datetime.now() + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 4. Decode JWT Token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        JSONResponse(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "false",
                "error": "Could not validate credentials",
            }
        )
