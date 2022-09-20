from functools import lru_cache
from typing import Literal

from pydantic import BaseSettings

class Settings(BaseSettings):
    mongo_conn_str: str = "mongodb://test:test1234@localhost:27017/"
    mongo_db: str = "access-ds"

    class Config:
        env_file = ".env"


# Get config settings
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()