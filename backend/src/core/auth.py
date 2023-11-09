from authlib.integrations.starlette_client import OAuth
from fastapi.security.open_id_connect_url import OpenIdConnect

import core.settings

oauth = OAuth()
oauth.register(
    name="orcid",
    server_metadata_url=core.settings.orcid_discovery_url,
    client_kwargs={"scope": "/authenticate"},
    client_id=core.settings.orcid_client_id, # if enabled, authlib will also check that the access token belongs to this client id (audience)
    client_secret=core.settings.orcid_client_secret,
)

fastapi_oauth2 = OpenIdConnect(
    openIdConnectUrl=core.settings.orcid_discovery_url,
    scheme_name="ORCID authentication",
    description="This OAuth2 server uses ORCID to authenticate users",
)