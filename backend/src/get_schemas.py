from pathlib import Path

import requests
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

import core
from models.json_schema import JsonSchemaUpdate
from models.schema_config import SchemaConfigUpdate



def get_list_from_github():
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


def get_schema_from_github(path):
    response = requests.get(core.settings.schema_download_url + path)
    if response.status_code == 200:
        try: 
            json = response.json()
            return json
        except:
            print(f"Failed to parse schema file '{path}'. Check if it is valid JSON. Skipping...")
            return None


def get_config_from_github():
    file = "/schema.conf.json"
    response = requests.get(core.settings.schema_download_url + file)
    if response.status_code == 200:
        print(f"Fetched schema configurations from github")
        return response.json()


async def get_json_schema_by_name(collection: AsyncIOMotorCollection, name: str):
    return await collection.find_one({"name": name})


async def create_json_schema(collection: AsyncIOMotorCollection, document: dict):
    name = document['$id'] if "$id" in document else document['resource']
    json_schema = JsonSchemaUpdate(
        name=name,
        data=document)
    print(f"Create in json_schemas: '{name}'")
    await collection.insert_one(json_schema.model_dump())


async def replace_json_schema(collection: AsyncIOMotorCollection, id: str, document: dict):
    name = document['$id'] if "$id" in document else document['resource']
    json_schema = JsonSchemaUpdate(
        name=name,
        data=document)
    print(f"Replace in json_schemas: '{name}'")
    await collection.replace_one({"_id": ObjectId(id)}, json_schema.model_dump())


async def get_config_by_name(collection: AsyncIOMotorCollection, name: str):
    return await collection.find_one({"name": name})


async def create_config(collection: AsyncIOMotorCollection, document: dict):
    name = document['name']
    config = SchemaConfigUpdate(**document)
    print(f"Create in schema_configs: '{name}'")
    await collection.insert_one(config.model_dump())


async def replace_config(collection: AsyncIOMotorCollection, id: str, document: dict):
    name = document['name']
    config = SchemaConfigUpdate(**document)
    print(f"Replace in schema_configs: '{name}'")
    await collection.replace_one({"_id": ObjectId(id)}, config.model_dump())


async def main():
    client = AsyncIOMotorClient(core.settings.mongo_conn_str)
    db = client[core.settings.mongo_db]
    json_schema_collection = db.json_schemas
    schema_config_collection = db.schema_configs

    # fetch list of schemas from github
    schemas = {}
    schema_list = get_list_from_github()

    for path in schema_list:
        s = get_schema_from_github(path)
        if s is not None and "$id" in s: 
            if s['$id'] in schemas:
                print(f"Found another instance of {s['$id']} in file '/{path}'. Skipping...")
            else: 
                schemas[s['$id']] = s
                print(f"Found schema '{s['$id']}' in file '/{path}'")

    if len(schemas) > 0:
        for s in schemas.values():
            # update if existing schema, otherwise create new
            existing = await get_json_schema_by_name(
                collection=json_schema_collection,
                name = s["$id"])
            if existing is None:
                await create_json_schema(
                    collection=json_schema_collection,
                    document=s)
            else:
                await replace_json_schema(
                    collection=json_schema_collection,
                    id=existing["_id"],
                    document=s)

    # fetch schema configurations from github
    configs = get_config_from_github()
    if len(configs) > 0:
        for c in configs:
            # resolve json-schema
            json_schema = await get_json_schema_by_name(
                collection=json_schema_collection,
                name = c["json_schema"])
            if json_schema is None:
                raise Exception(f"Schema config {c['name']} refers to inexistent JSON schema '{c['json_schema']}'")
            c['json_schema'] = str(json_schema["_id"])
            # update if existing config, otherwise create new
            existing = await get_config_by_name(
                    collection=schema_config_collection,
                    name = c["name"])
            if existing is None:
                await create_config(
                    collection=schema_config_collection,
                    document=c)
            else:
                await replace_config(
                    collection=schema_config_collection,
                    id=existing["_id"],
                    document=c)


if __name__ == '__main__' and __package__ is None:
    loop = asyncio.run(main())
