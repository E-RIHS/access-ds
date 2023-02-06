from typing import Optional, List
import json

from fastapi import APIRouter, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError

import core
#import core.utils.jsonschema
#import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/schema",
    tags=["schema"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/")
async def get_all_schemas():
    """
    Return all schemas.
    """
    response = await crud.schema.search(
        collection=db.schemas)
    return response


@router.get("/{id}")
async def get_schema_by_id(
        id: str = Path(None, description="The id of the schema")):
    """
    Return a single schema by its id.
    """
    try:
        response = await crud.schema.get(
            collection=db.schemas, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("/")
async def create_schema(schema: dict):
    """
    Create a new schema.
    """
    try:
        # validate agains resource and category models
        #schema_instance = models.SchemaUpdate(**schema)
        #await core.utils.jsonschema.validate_instance(schema, validate_category=True)

        # create the schema
        response = await crud.schema.create(
            collection=db.schemas,
            data=schema)
    # except ValidationError as err:
    #     raise HTTPException(status_code=422, detail=err.errors())
    # except core.utils.jsonschema.SchemaValidationError as err:
    #     raise HTTPException(status_code=422, detail=err.args[0])
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="NotCreated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}")
async def replace_schema(
        schema: dict,
        id: str = Path(None, description="The id of the schema")):
    """
    Replace a schema (full update).
    """
    try:
        # validate agains resource and category models
        #collection_resource_instance = models.CollectionUpdate(**collection)
        #await core.utils.jsonschema.validate_instance(collection, validate_category=True)

        # update the schema
        updated = await crud.schema.replace(
            collection=db.schemas, 
            id=id,
            data=schema)
    # except ValidationError as err:
    #     raise HTTPException(status_code=422, detail=err.errors())
    # except core.utils.jsonschema.SchemaValidationError as err:
    #     raise HTTPException(status_code=422, detail=err.args[0])
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="NotUpdated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return updated


@router.delete("/{id}")
async def delete_schema(
        id: str = Path(None, description="The id of the schema")):
    """
    Delete a schema.
    """
    try:
        deleted = await crud.schema.remove(
            collection=db.schemas, 
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