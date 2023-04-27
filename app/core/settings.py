from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""

    class Config:
        env_file=".env"

@lru_cache(maxsize=None)
def get_config():
    return Settings()


settings = get_config()