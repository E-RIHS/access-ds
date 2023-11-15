from typing import Optional
import urllib.parse

from fastapi import APIRouter, Request, HTTPException, Depends, Path, Query, status
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient

import core
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"])


@router.get("/login")
async def login(request: Request, uiroute: Optional[str] = None):
    '''
    This endpoint will redirect the user to ORCID to authenticate.
    When the user is authenticated, ORCID respond to the redirect url with a CODE,
    which is then used to obtain an access token.
    '''
    redirect_uri = f"{core.settings.api_url}/api/auth/token"
    if uiroute is not None:
        redirect_uri = f"{redirect_uri}?uiroute={uiroute}"
    return await core.oauth.orcid.authorize_redirect(request, redirect_uri)


@router.get("/token")
async def get_token(request: Request, uiroute: Optional[str] = None):
    '''
    Obtain the access and id tokens from ORCID.
    After the user is authenticated, ORCID will redirect to this endpoint with a CODE
    which will be used to request the tokens from ORCID (so called 3-legged OAuth).
    '''
    # get the access token from ORCID
    token_response = await core.oauth.orcid.authorize_access_token(request)
    # build the redirect url
    if uiroute is None:
        redirect_uri = f"{core.settings.api_url}/api/auth/userinfo"
    else:
        redirect_uri = f"{core.settings.frontend_url}/callback?route={uiroute}&token={token_response['access_token']}&name={token_response['name']}&orcid={token_response['orcid']}"
    # redirect to the url
    return RedirectResponse(redirect_uri)


@router.get("/userinfo")
async def show_userinfo(request: Request, token: Optional[str] = Depends(core.fastapi_oauth2)):
    print(token)
    try:
        # query ORCID to give us some information about the user
        user = await core.oauth.orcid.userinfo(token={"access_token": token})
    except Exception as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Supplied authentication could not be validated ({exp})",
        )
    return user