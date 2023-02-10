from functools import lru_cache
from typing import Literal

from pydantic import BaseSettings

class Settings(BaseSettings):
    mongo_conn_str: str = "mongodb://test:test1234@localhost:27017/"
    mongo_db: str = "access-ds"
    schema_file_list_url: str = "https://api.github.com/repos/E-RIHS/schema/git/trees/main?recursive=1"
    schema_download_url: str = "https://raw.githubusercontent.com/E-RIHS/schema/main/"

    class Config:
        env_file = ".env"


# Get config settings
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()