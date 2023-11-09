from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/ui_schema",
    tags=["UI Schema"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/", response_model=models.UiSchemaList)
async def get_all_ui_schemas():
    """
    Return all UI Schemas.
    """
    response = await crud.ui_schema.search(
        collection=db.ui_schemas,
        limit=0)
    return response


@router.get("/{id}", response_model=models.UiSchema)
async def get_ui_schema_by_id(
        id: str = Path(description="The id of the schema")):
    """
    Return a single UI Schema by its id.
    """
    try:
        response = await crud.ui_schema.get(
            collection=db.ui_schemas, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}/name", response_model=models.UiSchemaShort)
async def get_ui_schema_name(
        id: str = Path(description="The id of the schema")):
    """
    Return the name of a UI Schema by its id.
    """
    try:
        response = await crud.ui_schema.get(
            collection=db.ui_schemas, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("/", response_model=models.UiSchema)
async def create_ui_schema(
        data: models.UiSchemaUpdate):
    """
    Create a new UI Schema.
    """
    try:
        # create the schema
        response = await crud.ui_schema.create(
            collection=db.ui_schemas,
            data=data)
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="NotCreated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}", response_model=models.UiSchema)
async def replace_ui_schema(
        data: models.UiSchemaUpdate,
        id: str = Path(description="The id of the schema")):
    """
    Replace a UI Schema (full update).
    """
    try:
        # update the schema
        updated = await crud.ui_schema.replace(
            collection=db.ui_schemas, 
            id=id,
            data=data)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="NotUpdated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return updated


@router.delete("/{id}", response_model=models.UiSchema)
async def delete_ui_schema(
        id: str = Path(description="The id of the schema")):
    """
    Delete a UI Schema.
    """
    try:
        deleted = await crud.ui_schema.remove(
            collection=db.ui_schemas, 
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