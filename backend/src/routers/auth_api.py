from typing import Optional, List
import json
import urllib.parse

from fastapi import APIRouter, Request, HTTPException, Depends, Path, Query, status
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
async def auth(request: Request, api_callback: bool = True):
    '''
    This endpoint will redirect the user to ORCID to authenticate.
    When the user is authenticated, ORCID respond to the redirect url with a CODE,
    which is then used to obtain an access token.
    '''
    # urlencode the callback url
    if api_callback:
        callback = f"{core.settings.api_url}/auth/userinfo"
    else:
        callback = f"{core.settings.frontend_url}/callback"
    callback = urllib.parse.quote(callback, safe="")
    redirect_uri = f"{core.settings.api_url}/auth/token?callback={callback}"
    return await core.oauth.orcid.authorize_redirect(request, redirect_uri)


@router.get("/token")
async def auth_callback(request: Request, callback: str):
    '''
    Obtain the access and id tokens from ORCID.
    After the user is authenticated, ORCID will redirect to this endpoint with a CODE
    which will be used to request the tokens from ORCID (so called 3-legged OAuth).
    '''
    token_response = await core.oauth.orcid.authorize_access_token(request)
    #return {"response": response, "callback": callback}
    #redirect to the callback url with the access token in the header
    return token_response


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