from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/default_dataset",
    tags=["Default datasets for JSON Schema"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/", response_model=models.DefaultDatasetList)
async def get_all_default_datasets():
    """
    Return all default datasets for JSON schemas.
    """
    response = await crud.default_dataset.search(
        collection=db.default_datasets,
        limit=0)
    return response


@router.get("/{id}", response_model=models.DefaultDataset)
async def get_default_dataset_by_id(
        id: str = Path(description="The id of the default dataset")):
    """
    Return a single default dataset by its id.
    """
    try:
        response = await crud.default_dataset.get(
            collection=db.default_datasets, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}/name", response_model=models.DefaultDatasetShort)
async def get_default_dataset_name(
        id: str = Path(description="The id of the default dataset")):
    """
    Return the name of a default dataset by its id.
    """
    try:
        response = await crud.default_dataset.get(
            collection=db.default_datasets, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("/", response_model=models.DefaultDataset)
async def create_default_dataset(
        data: models.DefaultDatasetUpdate):
    """
    Create a new default dataset.
    """
    try:
        # create the schema
        response = await crud.default_dataset.create(
            collection=db.default_datasets,
            data=data)
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="NotCreated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}", response_model=models.DefaultDataset)
async def replace_default_dataset(
        data: models.DefaultDatasetUpdate,
        id: str = Path(description="The id of the default dataset")):
    """
    Replace a default dataset Schema (full update).
    """
    try:
        # update the schema
        updated = await crud.default_dataset.replace(
            collection=db.default_datasets, 
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


@router.delete("/{id}", response_model=models.DefaultDataset)
async def delete_default_dataset(
        id: str = Path(description="The id of the default dataset")):
    """
    Delete a default dataset.
    """
    try:
        deleted = await crud.default_dataset.remove(
            collection=db.default_datasets, 
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