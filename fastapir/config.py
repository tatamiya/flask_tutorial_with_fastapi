from pydantic import BaseSettings


class Settings(BaseSettings):
    session_secret_key: str

    class Config:
        env_file = ".env"
