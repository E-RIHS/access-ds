from pathlib import Path

import requests
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

import core


def get_list():
    schema_list = []
    response = requests.get(core.settings.schema_file_list_url)
    if response.status_code == 200:
        response_data = response.json()
        for file in response_data["tree"]:
            if file["type"] == "blob":
                extensions = Path(file["path"]).suffixes
                extensions.reverse()
                if extensions[0] == ".json" and extensions[1] == ".schema":
                    schema_list.append(file['path'])
    return schema_list


def get_schema(path):
    response = requests.get(core.settings.schema_download_url + path)
    if response.status_code == 200:
        return response.json()


async def drop_schema_collection(db: AsyncIOMotorDatabase):
    existing_collections = await db.list_collection_names()
    if "schemas" in existing_collections:
        print("Drop schemas collection in database")
        await db.drop_collection("schemas")


async def store_schema_in_db(db: AsyncIOMotorDatabase, schema: dict):
    print(f"Store schema '{schema['$id']}'")
    await db.schemas.insert_one(schema)


async def main():
    client = AsyncIOMotorClient(core.settings.mongo_conn_str)
    db = client[core.settings.mongo_db]

    schema_list = get_list()
    schemas = {}

    for path in schema_list:
        s = get_schema(path)
        if "$id" in s: 
            if s['$id'] in schemas:
                raise Exception(f"Found another instance of {s['$id']} in file '/{path}'")
            schemas[s['$id']] = s
            print(f"Found schema '{s['$id']}' in file '/{path}'")

    if len(schemas) > 0:
        await drop_schema_collection(db)
        for s in schemas.values():
            await store_schema_in_db(db, s)


if __name__ == '__main__' and __package__ is None:
    loop = asyncio.run(main())
