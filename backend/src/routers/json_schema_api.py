from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/json_schema",
    tags=["JSON Schema"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/", response_model=models.JsonSchemaList)
async def get_all_json_schemas():
    """
    Return all JSON Schemas.
    """
    response = await crud.json_schema.search(
        collection=db.json_schemas,
        limit=0)
    return response


@router.get("/{id}", response_model=models.JsonSchema)
async def get_json_schema_by_id(
        id: str = Path(description="The id of the schema")):
    """
    Return a single JSON Schema by its id.
    """
    try:
        response = await crud.json_schema.get(
            collection=db.json_schemas, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}/name", response_model=models.JsonSchemaShort)
async def get_json_schema_name(
        id: str = Path(description="The id of the schema")):
    """
    Return the name of a JSON Schema by its id.
    """
    try:
        response = await crud.json_schema.get(
            collection=db.json_schemas, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("/", response_model=models.JsonSchema)
async def create_json_schema(
        data: models.JsonSchemaUpdate):
    """
    Create a new JSON Schema.
    """
    try:
        # validate agains resource and category models
        #schema_instance = models.SchemaUpdate(**schema)
        #await core.utils.jsonschema.validate_instance(schema, validate_category=True)

        # create the schema
        response = await crud.json_schema.create(
            collection=db.json_schemas,
            data=data)
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


@router.put("/{id}", response_model=models.JsonSchema)
async def replace_json_schema(
        data: models.JsonSchemaUpdate,
        id: str = Path(description="The id of the schema")):
    """
    Replace a JSON Schema (full update).
    """
    try:
        # validate agains resource and category models
        #collection_resource_instance = models.CollectionUpdate(**collection)
        #await core.utils.jsonschema.validate_instance(collection, validate_category=True)

        # update the schema
        updated = await crud.json_schema.replace(
            collection=db.json_schemas, 
            id=id,
            data=data)
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


@router.delete("/{id}", response_model=models.JsonSchema)
async def delete_json_schema(
        id: str = Path(description="The id of the schema")):
    """
    Delete a JSON Schema.
    """
    try:
        deleted = await crud.json_schema.remove(
            collection=db.json_schemas, 
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