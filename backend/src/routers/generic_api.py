from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/generic",
    tags=["Generic record"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.post("/")
async def create_record(
        data: dict):
    """
    Create a new generic record.
    """
    # check for (existing) schema config in data
    if "$config" not in data:
        raise HTTPException(status_code=400, detail="MissingConfig")
    try:
        schema_config = await crud.schema_config.get(
            collection=db.schema_configs, 
            id=data["$config"])
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="InvalidConfig")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    # TODO: validate data using schema

    # create the record
    try:
        print(schema_config["resource"])
        response = await crud.generic.create(
            collection=db[schema_config["resource"].lower()],
            data=data)
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="NotCreated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response
