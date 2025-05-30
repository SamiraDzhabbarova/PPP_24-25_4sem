from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
