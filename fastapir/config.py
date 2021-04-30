import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    session_secret_key: str
    database_url: str = "sqlite:///./fastapir.db"
    connect_args: dict[str, bool] = {"check_same_thread": False}

    class Config:
        env_file = ".env"


if os.getenv("GAE_APPLICATION", None):
    settings = Settings(connect_args={})
else:
    settings = Settings()
