from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    RATE_LIMIT_MAX_REQUESTS: int
    RATE_LIMIT_WINDOW: int
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()
