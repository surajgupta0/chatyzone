from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt  # Install with `pip install PyJWT`

SECRET_KEY = "your_secret_key"  # Replace with a secure key

PUBLIC_ROUTES = [
    "/", 
    "/login", 
    "/register",
]

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        # ✅ Allow public routes without requiring a token
        if request.url.path in PUBLIC_ROUTES or request.url.path.startswith("/static"):
            return None  # No token required for public routes

        # 🔹 Extract credentials (JWT token)
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

        # 🔹 Verify JWT Token
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid or expired token.")

        return credentials.credentials

    def verify_jwt(self, token: str) -> bool:
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token has expired.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid token.")
