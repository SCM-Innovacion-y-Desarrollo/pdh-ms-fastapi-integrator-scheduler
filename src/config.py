import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DRIVER: str = "mysql+asyncmy"  # shouldn't be hardcoded
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASS")
    HOST: str = os.getenv("DB_HOST")
    PORT: str = os.getenv("DB_PORT", "3306")
    NAME: str = os.getenv("DB_NAME")
    CONN: str = os.getenv("DB_CONN", "tcp")  # tcp or socket, tcp by default


config = Settings()