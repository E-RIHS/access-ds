import json
from typing import Optional

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
def show_all_projects(request: Request):
    """
    Displaying a list of projects
    """
    return templates.TemplateResponse("project_list.html.jinja", {
        "request": request
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
        schema = modify_project(role=role, draft=draft)
    else:
        schema = project_schema

    return templates.TemplateResponse("project_form.html.jinja", {
        "request": request,
        "schema": json.dumps(schema),
        "id": "",
        "title": "Project"
    })


@router.get("/project/{id}", response_class=HTMLResponse)
def show_project_with_id(
        request: Request, 
        id: str = Path(None, description="Project identifier")):
    """
    Displaying project form with existing data, accessed by its id
    """
    return templates.TemplateResponse("template_form.html.jinja", {
        "request": request,
        "schema": json.dumps(project_schema),
        "id": id,
        "title": "Project"
    })