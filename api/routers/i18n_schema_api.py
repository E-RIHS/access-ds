from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/i18n_schema",
    tags=["i18n Schema"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/", response_model=models.I18nSchemaList)
async def get_all_i18n_schemas():
    """
    Return all i18n Schemas.
    """
    response = await crud.i18n_schema.search(
        collection=db.i18n_schemas,
        limit=0)
    return response


@router.get("/{id}", response_model=models.I18nSchema)
async def get_i18n_schema_by_id(
        id: str = Path(None, description="The id of the schema")):
    """
    Return a single i18n Schema by its id.
    """
    try:
        response = await crud.i18n_schema.get(
            collection=db.i18n_schemas, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("/", response_model=models.I18nSchema)
async def create_i18n_schema(
        data: models.I18nSchemaUpdate):
    """
    Create a new i18n Schema.
    """
    try:
        # create the schema
        response = await crud.i18n_schema.create(
            collection=db.i18n_schemas,
            data=data)
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="NotCreated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}", response_model=models.I18nSchema)
async def replace_i18n_schema(
        data: models.I18nSchemaUpdate,
        id: str = Path(None, description="The id of the schema")):
    """
    Replace a i18n Schema (full update).
    """
    try:
        # update the schema
        updated = await crud.i18n_schema.replace(
            collection=db.i18n_schemas, 
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


@router.delete("/{id}", response_model=models.I18nSchema)
async def delete_i18n_schema(
        id: str = Path(None, description="The id of the schema")):
    """
    Delete a i18n Schema.
    """
    try:
        deleted = await crud.i18n_schema.remove(
            collection=db.i18n_schemas, 
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