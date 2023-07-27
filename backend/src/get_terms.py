from pathlib import Path

import requests
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

import core
from models.term import TermUpdate
#from models.schema_config import SchemaConfigUpdate


def get_list_from_github():
    files = []
    response = requests.get(core.settings.vocab_file_list_url)
    if response.status_code == 200:
        response_data = response.json()
        for file in response_data:
            if file["type"] == "file":
                extension = Path(file["name"]).suffix
                if extension.lower() == ".json":
                    files.append(file['download_url'])
    return files


def get_file_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    

async def create_or_replace_term(
        collection: AsyncIOMotorCollection, 
        term: TermUpdate): 
    # check if term exists
    # if yes, replace
    # if no, create new term
    existing = await collection.find_one({"name": term.name, "instance_of": term.instance_of})
    if existing:
        print(f"Replace term: '{term.name}' [{term.instance_of}]")
        await collection.replace_one({"_id": ObjectId(existing["_id"])}, term.dict())
    else:
        print(f"Create term: '{term.name}'")
        await collection.insert_one(term.dict())


async def main():
    client = AsyncIOMotorClient(core.settings.mongo_conn_str)
    db = client[core.settings.mongo_db]
    term_collection = db.terms

    # fetch list of controlled lists from github
    files = get_list_from_github()
    
    for file in files:
        print(f"Fetching '{file}'")
        data = get_file_from_github(file)
        if data:
            # create/update root term
            root_term = TermUpdate(
                name=data['id'],
                instance_of="_root",
                label={ 'en': data['id'].replace("_", " ").title() },
                description={ 'en': data['description'] }
            )
            await create_or_replace_term(term_collection, root_term)

            # create/update terms
            for term in data['terms'].values():
                term = TermUpdate(
                    name=term['term'],
                    instance_of=root_term.name,
                    label=term['label'],
                    description=term['description'] if 'description' in term else None,
                    same_as=term['sameAs'] if 'sameAs' in term else None,
                    source=term['source'] if 'source' in term else None
                )
                await create_or_replace_term(term_collection, term)

if __name__ == '__main__' and __package__ is None:
    loop = asyncio.run(main())
