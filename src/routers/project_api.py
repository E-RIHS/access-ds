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
    prefix="/api/project",
    tags=["project"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/")
async def get_all_projects():
    """
    Return all projects.
    """
    response = await crud.project.search(
        collection=db.projects)
    return response


@router.get("/{id}")
async def get_project_by_id(
        id: str = Path(None, description="The id of the project")):
    """
    Return a single project by its id.
    """
    try:
        response = await crud.project.get(
            collection=db.projects, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("/")
async def create_project(project: dict):
    """
    Create a new project.
    """
    try:
        # validate agains resource and category models
        #project_instance = models.projectUpdate(**project)
        #await core.utils.jsonschema.validate_instance(project, validate_category=True)

        # create the project
        response = await crud.project.create(
            collection=db.projects,
            data=project)
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
async def replace_project(
        project: dict,
        id: str = Path(None, description="The id of the project")):
    """
    Replace a project (full update).
    """
    try:
        # validate agains resource and category models
        #collection_resource_instance = models.CollectionUpdate(**collection)
        #await core.utils.jsonschema.validate_instance(collection, validate_category=True)

        # update the project
        updated = await crud.project.replace(
            collection=db.projects, 
            id=id,
            data=project)
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
async def delete_project(
        id: str = Path(None, description="The id of the project")):
    """
    Delete a project.
    """
    try:
        deleted = await crud.project.remove(
            collection=db.projects, 
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