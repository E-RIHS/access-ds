from typing import Optional, List
import json

from fastapi import APIRouter, HTTPException, Path, Query
from motor.motor_asyncio import AsyncIOMotorClient

import core
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/term",
    tags=["Terms"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/", response_model=models.TermList)
async def search_terms(
        skip: Optional[int] = Query(0, description="Skip the x first results"),
        limit: Optional[int] = Query(10, description="Return x results"), 
        find: Optional[str] = Query(None, description="Mongodb-style find query in JSON"),
        sort_by: Optional[List[str]] = Query(["name"], description="Sorting options (array of strings)"),
        sort_desc: Optional[List[bool]] = Query([], description="Sort descending (arry of booleans)")):
    """
    Search terms.
    """

    if find is not None:
        find = json.loads(find)
    else:
        find = {}

    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=400, detail="ParameterError")
    try: 
        response = await crud.term.search(
            collection=db.terms,
            find=find,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc)
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}", response_model=models.Term)
async def get_resolved_term_by_id(
        id: str = Path(description="The id of the term")):
    """
    Return a single, fully resolved term by its id.
    """
    try:
        response = await crud.term.get(
            collection=db.terms, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}/children", response_model=models.TermChildren)
async def get_child_terms(
    id: str = Path(description="The id of the term")):
    """
    Return all terms that are instances of this term.
    """

    response = await crud.term.get_children(
        collection=db.terms,
        parent_id=id)
    return { 'data': response }


@router.get("/{id}/children/{lang}", response_model=models.TermChildrenLocalised)
async def get_child_terms_localised(
    id: str = Path(description="The id of the term"),
    lang: str = Path(description="Language")):
    """
    Return all terms that are instances of this term (localised).
    """
    response = await crud.term.get_children_localised(
        collection=db.terms,
        parent_id=id,
        lang=lang.lower())
    return { 'data': response }


@router.post("/", response_model=models.Term)
async def create_term(
        data: models.TermUpdate):
    """
    Create a new term.
    """
    try:
        # create the term
        response = await crud.term.create(
            collection=db.terms,
            data=data)
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="NotCreated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}", response_model=models.Term)
async def replace_term(
        data: models.TermUpdate,
        id: str = Path(description="The id of the term")):
    """
    Replace a term (full update).
    """
    try:
        # update the term
        response = await crud.term.replace(
            collection=db.terms, 
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
    return response


@router.delete("/{id}", response_model=models.Term)
async def delete_term(
        id: str = Path(description="The id of the term")):
    """
    Delete a term.
    """
    try:
        deleted = await crud.term.remove(
            collection=db.terms, 
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
