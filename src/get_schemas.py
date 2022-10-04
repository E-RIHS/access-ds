from pathlib import Path
import json

import requests

import core
import crud


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


def store_schema_in_db(schema):
    pass



schema_list = get_list()
for path in schema_list:
    schema = get_schema(path)
    if "$id" in schema: 
        print(f"Schema '{schema['$id']}' in file '/{path}'")

# TODO: check if all $id's are unique (len of set)
# TODO: drop schemas
# TODO: store schemas

