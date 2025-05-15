from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/flexicmdb"
    SECRET_KEY: str = "your-secret-key"
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "https://*.vercel.app"]

class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"

    settings = Settings()
