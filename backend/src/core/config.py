from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Production App"
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    SECRET_KEY: str = "your_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    APP_NAME = "FastAPI Production App"
    DEBUG: bool = False
    TESTING: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

    