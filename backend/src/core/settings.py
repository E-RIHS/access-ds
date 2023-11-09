from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_conn_str: str = "mongodb://test:test1234@localhost:27017/"
    mongo_db: str = "access-ds"
    cors_origins: str = "http://localhost:8001"
    schema_file_list_url: str = "https://api.github.com/repos/E-RIHS/schema/git/trees/main?recursive=1"
    schema_download_url: str = "https://raw.githubusercontent.com/E-RIHS/schema/main/"
    terms_file_list_url: str = "https://api.github.com/repos/E-RIHS/controlled-lists/contents/json"
    orcid_discovery_url: str = "https://sandbox.orcid.org/.well-known/openid-configuration"
    orcid_client_id: str = "APP-TR5LKN7WUPO4DY6Q"
    orcid_client_secret: str = "d0b0b0e4-0b0b-0b0b-0b0b-0b0b0b0b0b0b" # This is a fake secret, replace with your own in .env

    class Config:
        env_file = ".env"


# Get config settings
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()