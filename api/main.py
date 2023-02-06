from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.datastructures import QueryParams

import routers


# Main API application
app = FastAPI(
    title="Access-DS",
    description="E-RIHS access documentation system",
    version="0.1",
    contact={
        "name": "IPERION HS Task 6.3 team, Wim Fremout",
        "url": "https://github.com/E-RIHS/access-ds",
        "email": "wim.fremout@kikirpa.be",
    }
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Adding some routes to our main application
app.include_router(routers.json_schema_api.router)
app.include_router(routers.ui_schema_api.router)
app.include_router(routers.i18n_schema_api.router)
app.include_router(routers.default_dataset_api.router)
app.include_router(routers.schema_config_api.router)
#app.include_router(routers.default_schema_api.router)
app.include_router(routers.project_api.router)
app.include_router(routers.ui.router)


@app.middleware("http")
async def fix_list_query_params(request: Request, call_next):
    '''
    Axios and some other libs put square brackets on list parameters, 
    FastAPI/Starlette do no support this. This middleware removes the
    brackets.
    Based on code in https://github.com/tiangolo/fastapi/issues/739
    '''
    def fix_key(key: str):
        if key and key.endswith("[]"):
            key = key[:-2]
        return key

    request._query_params = QueryParams(
        [(fix_key(key), value) for key, value in request.query_params.multi_items()]
    )
    request.scope["query_string"] = str(request.query_params).encode("ascii")
    response = await call_next(request)
    return response