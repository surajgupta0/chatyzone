from fastapi import FastAPI
from .core import variables
from .core.database import MongoManager
from .routes import auth, file, chat, summarize, folder, settings as user_settings
from fastapi.middleware.cors import CORSMiddleware
from .middleware.LoggingMiddleware import LoggingMiddleware
from fastapi.staticfiles import StaticFiles
from .middleware.security import JWTBearer
from contextlib import asynccontextmanager
from .core.variables import BASE_UPLOAD_DIR

#Lifespan manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongodb = MongoManager()
    yield
    await app.state.mongodb.close()
    
# Initialize FastAPI
app = FastAPI(
    lifespan    = lifespan,
    title       = variables.PROJECT_NAME,
    description = variables.PROJECT_DESCRIPTION,
    version     = variables.VERSION,
)

# Middleware for CORS
# This allows cross-origin requests, which is useful for development
app.add_middleware(CORSMiddleware, 
    allow_origins       = ["*"],  # Change this in production!
    allow_credentials   = True,
    allow_methods       = ["*"],
    allow_headers       = ["*"]
)

# Middleware for logging requests and responses
app.middleware(LoggingMiddleware)
# app.add_middleware(JWTBearer) 


# Route handlers
app.include_router(auth.router)
app.include_router(file.router)
app.include_router(chat.router)# app.include_router(summarize.router)
app.include_router(folder.router)
# app.include_router(user_settings.router)

# app.mount("/static", StaticFiles(directory=BASE_UPLOAD_DIR), name="static")