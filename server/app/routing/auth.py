from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.di.auth_service import get_auth_service
from app.services.auth import AbstractAuthService, TokenSet


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    access_token_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int


auth_router = APIRouter()


@auth_router.post("/login")
async def login(
    form: LoginRequest,
    auth_service: Annotated[AbstractAuthService, Depends(get_auth_service)],
) -> TokenSet:
    try:
        token_set = await auth_service.login(form.username, form.password)
    except AbstractAuthService.UserNotFound:
        raise HTTPException(400, "User not found")
    except AbstractAuthService.InvalidPassword:
        raise HTTPException(400, "Invalid password")
    return token_set
