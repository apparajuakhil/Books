from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, '../../books.db')}"
    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
