import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_settings: dict = {}
    session_secret_key: str
    database_url: str = "sqlite:///./fastapir.db"
    connect_args: dict[str, bool] = {"check_same_thread": False}

    class Config:
        env_file = ".env"


if os.getenv("GAE_APPLICATION", None):
    settings = Settings(
        app_settings={"openapi_url": None},
        connect_args={},
    )
else:
    settings = Settings()
