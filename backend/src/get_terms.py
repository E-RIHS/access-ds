from pathlib import Path
from typing import Optional

import requests
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

import core
from models.term import Term, TermUpdate


#root_oid = ObjectId(bytes(core.settings.root_term_object_id, 'utf-8'))
root_term = {
    'name': '_root',
    'instance_of': None,
    'label': { 'en': '(root)'}
}


def get_list_from_github():
    files = []
    response = requests.get(core.settings.terms_file_list_url)
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
        term: Optional[TermUpdate] = None):
    # check if term exists
    if term:
        term = term.dict()
        existing = await collection.find_one({"name": term['name'], "instance_of": term['instance_of']})
    else:
        term = root_term
        existing = await collection.find_one({"instance_of": None})
    # if exists, replace
    # if not, create new term
    if existing:
        result = await collection.replace_one({"_id": ObjectId(existing["_id"])}, term)
        if result.modified_count == 1:
            print(f"  - Replaced term: '{term['name']}'")
            return str(existing["_id"])
    else:
        result = await collection.insert_one(term)
        if result.inserted_id:
            print(f"  - Created term: '{term['name']}'")
            return str(result.inserted_id)
    return None
 

async def main():
    client = AsyncIOMotorClient(core.settings.mongo_conn_str)
    db = client[core.settings.mongo_db]
    term_collection = db.terms

    # create/update root term
    root_oid = await create_or_replace_term(term_collection)

    # fetch list of controlled lists from github
    files = get_list_from_github()
    
    for file in files:
        print(f"Fetching '{file}'")
        data = get_file_from_github(file)
        if data:
            # create/update parent term
            parent_term = TermUpdate(
                name=data['id'],
                instance_of=str(root_oid),
                label={ 'en': data['id'].replace("_", " ").title() },
                description={ 'en': data['description'] }
            )
            parent_id = await create_or_replace_term(term_collection, parent_term)

            # create/update terms
            for term in data['terms'].values():
                term = TermUpdate(
                    name=term['term'],
                    instance_of=parent_id,
                    label=term['label'],
                    description=term['description'] if 'description' in term else None,
                    same_as=term['sameAs'] if 'sameAs' in term else None,
                    source=term['source'] if 'source' in term else None
                )
                await create_or_replace_term(term_collection, term)


if __name__ == '__main__' and __package__ is None:
    loop = asyncio.run(main())
