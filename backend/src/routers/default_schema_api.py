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
    prefix="/api/default_schema",
    tags=["default_schema"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/")
async def get_all_default_schemas():
    """
    Return all default schemas.
    """
    response = await crud.default_schema.search(
        collection=db.default_schemas)
    return response


@router.get("/{id}")
async def get_default_schema_by_id(
        id: str = Path(description="The id of the default_schema")):
    """
    Return a single default schema by its id.
    """
    try:
        response = await crud.default_schema.get(
            collection=db.default_schemas, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("/")
async def create_default_schema(default_schema: dict):
    """
    Create a new default schema.
    """
    try:
        # validate agains resource and category models
        #schema_instance = models.SchemaUpdate(**schema)
        #await core.utils.jsonschema.validate_instance(schema, validate_category=True)

        # create the default_schema
        response = await crud.default_schema.create(
            collection=db.default_schemas,
            data=default_schema)
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
async def replace_default_schema(
        default_schema: dict,
        id: str = Path(description="The id of the default_schema")):
    """
    Replace a default schema (full update).
    """
    try:
        # validate agains resource and category models
        #collection_resource_instance = models.CollectionUpdate(**collection)
        #await core.utils.jsonschema.validate_instance(collection, validate_category=True)

        # update the default_schema
        updated = await crud.default_schema.replace(
            collection=db.default_schemas, 
            id=id,
            data=default_schema)
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
async def delete_default_schema(
        id: str = Path(description="The id of the default_schema")):
    """
    Delete a default schema.
    """
    try:
        deleted = await crud.default_schema.remove(
            collection=db.default_schemas, 
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