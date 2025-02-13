from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .http.auth import auth_router
from .http.profile import profile_router
from .di.settings import get_settings

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
        401 "access_token_poisoned"
    
    Email verification request is a special. We use a token for identifying user that requests a verification. Possible errors:
    If access token not present:
        401 "access_token_not_present"
    If access token parsing and verifying failed:
        401 "access_token_invalid"
    If access token hasn't access to email verification resource:
        403 "access_token_forbidden", resource: "EMAIL_VERIFICATION"
    If access token user doesn't exist:
        401 "access_token_poisoned\""""
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().allow_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth")
app.include_router(profile_router, prefix="/profile")
