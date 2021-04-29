from pydantic import BaseSettings


class Settings(BaseSettings):
    session_secret_key: str
    database_url: str = "sqlite:///./fastapir.db"

    class Config:
        env_file = ".env"
