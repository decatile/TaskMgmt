from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routing.auth import auth_router
from .routing.profile import profile_router
from .di.settings import get_settings

app = FastAPI()
if get_settings().is_dev:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.include_router(auth_router, prefix="/auth")
app.include_router(profile_router, prefix="/profile")
