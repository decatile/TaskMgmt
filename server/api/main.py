from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.di.runtime_settings import get_runtime_settings
from api.di.session import get_settings
from .http.auth import auth_router
from .http.profile import profile_router

app = FastAPI(
    description="""
    Every authorized request firstly goes through token validation. Possible errors:
    If access token not present:
        401 "access_token_not_present"
    If access token parsing and verifying failed:
        401 "access_token_invalid"
    If access token hasn't access to API resource:
        403 "access_token_forbidden", resource: "API"
    If access token user doesn't exist:
        401 "access_token_poisoned\"""",
)

if not get_runtime_settings().gen_docs:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().allow_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth_router, prefix="/auth")
app.include_router(profile_router, prefix="/profile")
