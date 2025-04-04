import os

#Basic  Information
PROJECT_NAME                  : str = "pdf-chatifizer"
PROJECT_DESCRIPTION           : str = "A web application to chat with PDF documents."
VERSION                       : str = "1.0.0"
PORT                          : int = os.getenv("PORT", 8000)

# MongoDB Configuration
MONGO_USERNAME                : str = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD                : str = os.getenv("MONGO_PASSWORD")
MONGO_HOST                    : str = os.getenv("MONGO_HOST")
MONGO_PORT                    : str = os.getenv("MONGO_PORT")
MONGO_DB                      : str = os.getenv("MONGO_DB")

# OpenAI API Configuration
OPENAI_API_KEY                : str = os.getenv("OPENAI_API_KEY")

# FastAPI Configuration
DEBUG                         : bool = os.getenv("DEBUG", False)
HOST                          : str = os.getenv("HOST", "http://localhost")

# JWT Configuration
SECRET_KEY                    : str = os.getenv("SECRET_KEY")
ALGORITHM                     : str = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES   : str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 24*60)  # 24 hours

BASE_UPLOAD_DIR               : str = "src/uploads"
