from typing import Optional, List
import json

from fastapi import APIRouter, HTTPException, Path, Query
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

import core
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/schema_config",
    tags=["JSON Schema configuration sets"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


async def resolveSchema(collection: AsyncIOMotorCollection, crud_instance, schema_id: str):
    if schema_id is not None:
        response = await crud_instance.get(
            collection=collection,
            id=schema_id)
        return response
    else:
        return None


@router.get("/", response_model=models.SchemaConfigList)
async def search_schema_configs(
        skip: Optional[int] = Query(0, description="Skip the x first results"),
        limit: Optional[int] = Query(10, description="Return x results"), 
        find: Optional[str] = Query(None, description="Mongodb-style find query in JSON"),
        sort_by: Optional[List[str]] = Query(["name"], description="Sorting options (array of strings)"),
        sort_desc: Optional[List[bool]] = Query([], description="Sort descending (arry of booleans)")):
    """
    Search JSON Schema configuration sets.
    """

    if find is not None:
        find = json.loads(find)
    else:
        find = {}

    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=400, detail="ParameterError")
    try: 
        response = await crud.schema_config.search(
            collection=db.schema_configs,
            find=find,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc)
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}", response_model=models.SchemaConfig)
async def get_resolved_schema_config_by_id(
        id: str = Path(description="The id of the schema configuration set")):
    """
    Return a single, fully resolved JSON Schema configuration set by its id.
    """
    try:
        response = await crud.schema_config.get(
            collection=db.schema_configs, 
            id=id)
        # resolve schemas
        response["json_schema_resolved"] = await resolveSchema(db.json_schemas, crud.json_schema, response["json_schema"])
        response["ui_schema_resolved"] = await resolveSchema(db.ui_schemas, crud.ui_schema, response["ui_schema"])
        response["i18n_schema_resolved"] = await resolveSchema(db.i18n_schemas, crud.i18n_schema, response["i18n_schema"])
        response["default_dataset_resolved"] = await resolveSchema(db.default_dataset, crud.default_dataset, response["default_dataset"])
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("/", response_model=models.SchemaConfig)
async def create_schema_config(
        data: models.SchemaConfigUpdate):
    """
    Create a new JSON Schema configuration set.
    """
    try:
        # create the schema
        response = await crud.schema_config.create(
            collection=db.schema_configs,
            data=data)
        # resolve schemas
        response["json_schema_resolved"] = await resolveSchema(db.json_schemas, crud.json_schema, response["json_schema"])
        response["ui_schema_resolved"] = await resolveSchema(db.ui_schemas, crud.ui_schema, response["ui_schema"])
        response["i18n_schema_resolved"] = await resolveSchema(db.i18n_schemas, crud.i18n_schema, response["i18n_schema"])
        response["default_dataset_resolved"] = await resolveSchema(db.default_dataset, crud.default_dataset, response["default_dataset"])
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="NotCreated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}", response_model=models.SchemaConfig)
async def replace_schema_config(
        data: models.SchemaConfigUpdate,
        id: str = Path(description="The id of the schema")):
    """
    Replace a JSON Schema configuration set (full update).
    """
    try:
        # update the schema
        response = await crud.schema_config.replace(
            collection=db.schema_configs, 
            id=id,
            data=data)
        # resolve schemas
        response["json_schema_resolved"] = await resolveSchema(db.json_schemas, crud.json_schema, response["json_schema"])
        response["ui_schema_resolved"] = await resolveSchema(db.ui_schemas, crud.ui_schema, response["ui_schema"])
        response["i18n_schema_resolved"] = await resolveSchema(db.i18n_schemas, crud.i18n_schema, response["i18n_schema"])
        response["default_dataset_resolved"] = await resolveSchema(db.default_dataset, crud.default_dataset, response["default_dataset"])
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="NotUpdated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.delete("/{id}", response_model=models.SchemaConfig)
async def delete_schema_config(
        id: str = Path(description="The id of the schema")):
    """
    Delete a JSON Schema configuration set.
    """
    try:
        deleted = await crud.schema_config.remove(
            collection=db.schema_configs, 
            id=id)
    except crud.DependentObjectsError:
        raise HTTPException(status_code=400, detail="DependentObjects")
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except crud.NotDeletedError:
        raise HTTPException(status_code=400, detail="NotDeleted")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return deleted