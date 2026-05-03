from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_URL: str
    AI_SERVICE_URL: str
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
