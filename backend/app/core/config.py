from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Notes CRUD API"
    API_V1_STR: str = "/api/v1"
    
    MONGO_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "notes_db"
    
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
