import json
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.param_functions import Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

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

project_schema = "{}"


@router.get("/project", response_class=HTMLResponse)
def show_all_projects(request: Request):
    """
    Displaying a list of projects
    """
    return templates.TemplateResponse("project_list.html.jinja", {
        "request": request
    })


@router.get("/project/new", response_class=HTMLResponse)
def show_new_project(request: Request):
    """
    Displaying project form for new data entry
    """
    return templates.TemplateResponse("project_form.html.jinja", {
        "request": request,
        "schema": project_schema,
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
        "schema": project_schema,
        "id": id,
        "title": "Project"
    })