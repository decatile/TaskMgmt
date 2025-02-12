from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routing.auth import auth_router
from .routing.profile import profile_router
from .di.settings import get_settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().allow_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth")
app.include_router(profile_router, prefix="/profile")
