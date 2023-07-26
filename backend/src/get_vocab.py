from pathlib import Path

import requests
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

import core
#from models.json_schema import JsonSchemaUpdate
#from models.schema_config import SchemaConfigUpdate


def get_list_from_github():
    vocab_list = []
    response = requests.get(core.settings.vocab_file_list_url)
    if response.status_code == 200:
        response_data = response.json()
        for file in response_data:
            if file["type"] == "file":
                extension = Path(file["path"]).suffix
                if extension.lower() == ".json":
                    vocab_list.append(file['download_url'])
    return vocab_list



async def main():
    client = AsyncIOMotorClient(core.settings.mongo_conn_str)
    db = client[core.settings.mongo_db]
    vocab_collection = db.vocabularies

    # fetch list of controlled lists from github
    vocab_list = get_list_from_github()
    print(f"Found {len(vocab_list)} controlled lists on github")