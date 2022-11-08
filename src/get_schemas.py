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


def get_default_schemas():
    file = "/default_schema.conf.json"
    response = requests.get(core.settings.schema_download_url + file)
    if response.status_code == 200:
        print(f"Fetched default schemas in file {file}")
        return response.json()


async def drop_collection(db: AsyncIOMotorDatabase, collection: str):
    existing_collections = await db.list_collection_names()
    if collection in existing_collections:
        print(f"Drop {collection} collection in database")
        await db.drop_collection(collection)


async def store(db: AsyncIOMotorDatabase, collection: str, document: dict):
    name = document['$id'] if "$id" in document else document['resource']
    print(f"Store in {collection}: '{name}'")
    await db[collection].insert_one(document)


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
        await drop_collection(db=db, collection="schemas")
        for s in schemas.values():
            await store(db, "schemas", s)

    default_schemas = get_default_schemas()
    if len(default_schemas) > 0:
        await drop_collection(db=db, collection="default_schemas")
        for resource, default in default_schemas.items():
            document = {
                "resource": resource,
                "default": default
            }
            await store(db, "default_schemas", document)
            

if __name__ == '__main__' and __package__ is None:
    loop = asyncio.run(main())
