import json
from typing import Optional
from datetime import date, datetime

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.param_functions import Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from mergedeep import merge

import core
import crud

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="",
    tags=["ui"]
)

templates = Jinja2Templates(directory="templates")

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]

# TODO: temporarily load the json schema from a file
fh = open("./seeding/project.schema.json")
project_schema = json.load(fh)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def modify_project(role: Optional[str], state: Optional[str]):
    role_modifier = {}
    state_modifier = {}

    if role == "user":
        role_modifier["properties"] = {
            "id": {
                "readOnly": True
            },
            "version": {
                "readOnly": True
            },
            "state": {
                "readOnly": True
            },
            "assessment": {
                "readOnly": True
            },
            "creation_timestamp": {
                "readOnly": True
            },
            "creator": {
                "readOnly": True
            }
        }
    elif role == "reviewer":
        role_modifier["properties"] = {
            "id": {
                "readOnly": True
            },
            "version": {
                "readOnly": True
            },
            "state": {
                "enum": [
                    "accepted",
                    "revision requested",
                    "declined"
                ]
            },
            "creation_timestamp": {
                "readOnly": True
            },
            "creator": {
                "readOnly": True
            }
        }

    if state in ["accepted", "revision requested", "declined"]:
        state_modifier["readOnly"] = True

    return merge({}, project_schema, role_modifier, state_modifier)


@router.get("/project", response_class=HTMLResponse)
async def show_all_projects(request: Request):
    """
    Displaying a list of projects
    """
    try:
        response = await crud.project.get_all(
            collection=db.projects)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return templates.TemplateResponse("project_list.html.jinja", {
        "request": request,
        "response": json.dumps(response, default=json_serial)
    })


@router.get("/project/new", response_class=HTMLResponse)
def show_new_project(
        request: Request, 
        role: Optional[str] = Query(None, description="Role"),
        state: Optional[str] = Query(None, description="State")):
    """
    Displaying project form for new data entry
    """
    if role is not None or state is not None:
        schema = modify_project(role=role, state=state)
    else:
        schema = project_schema

    return templates.TemplateResponse("project_form.html.jinja", {
        "request": request,
        "schema": json.dumps(schema),
        "instance": "{}",
    })


@router.get("/project/{id}", response_class=HTMLResponse)
async def show_project_with_id(
        request: Request, 
        id: str = Path(None, description="Project identifier")):
    """
    Displaying project form with existing data, accessed by its id
    """
    try:
        response = await crud.project.get(
            collection=db.projects,
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))

    return templates.TemplateResponse("project_form.html.jinja", {
        "request": request,
        "schema": json.dumps(project_schema),
        "instance": json.dumps(response, default=json_serial),
    })