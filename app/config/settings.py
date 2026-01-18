from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    MONGODB_URL: str
    DATABASE_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()