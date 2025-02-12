from fastapi import FastAPI
from .routing.auth import auth_router
from .routing.profile import profile_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(profile_router, prefix="/profile")
