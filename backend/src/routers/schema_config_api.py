from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

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


@router.get("/", response_model=models.SchemaConfigList)
async def get_all_schema_configs():
    """
    Return all JSON Schema configuration sets.
    """
    response = await crud.schema_config.search(
        collection=db.schema_configs,
        limit=0)
    return response


@router.get("/{id}", response_model=models.SchemaConfig)
async def get_resolved_schema_config_by_id(
        id: str = Path(None, description="The id of the schema configuration set")):
    """
    Return a single, fully resolved JSON Schema configuration set by its id.
    """
    try:
        response = await crud.schema_config.get(
            collection=db.schema_configs, 
            id=id)
        # resolve json_schema
        json_schema = await crud.json_schema.get(
            collection=db.json_schemas,
            id=response["json_schema"])
        response["json_schema_resolved"] = json_schema["data"]
        # resolve ui_schema
        if response["ui_schema"] is not None:
            ui_schema = await crud.ui_schema.get(
                collection=db.ui_schemas,
                id=response["ui_schema"])
            response["ui_schema_resolved"] = ui_schema["data"]
        # resolve i18n_schema
        if response["ui_schema"] is not None:
            i18n_schema = await crud.i18n_schema.get(
                collection=db.i18n_schemas,
                id=response["i18n_schema"])
            response["i18n_schema_resolved"] = i18n_schema["data"]
        # resolve default_dataset
        if response["default_dataset"] is not None:
            default_dataset = await crud.default_dataset.get(
                collection=db.default_dataset,
                id=response["default_dataset"])
            response["default_dataset_resolved"] = default_dataset["data"]
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
        id: str = Path(None, description="The id of the schema")):
    """
    Replace a JSON Schema configuration set (full update).
    """
    try:
        # update the schema
        updated = await crud.schema_config.replace(
            collection=db.schema_configs, 
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


@router.delete("/{id}", response_model=models.SchemaConfig)
async def delete_schema_config(
        id: str = Path(None, description="The id of the schema")):
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