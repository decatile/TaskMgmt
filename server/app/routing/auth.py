from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.di.auth_service import get_auth_service
from app.dto.auth import LoginRequest, RegisterRequest, response_from_set
from app.services.auth import AbstractAuthService


auth_router = APIRouter()


@auth_router.post("/login")
async def login(
    form: LoginRequest,
    auth_service: Annotated[AbstractAuthService, Depends(get_auth_service)],
) -> JSONResponse:
    try:
        token_set = await auth_service.login(form.email, form.password)
    except AbstractAuthService.UserNotFound:
        raise HTTPException(400, "User not found")
    except AbstractAuthService.InvalidPassword:
        raise HTTPException(400, "Invalid password")
    return response_from_set(token_set)


@auth_router.post("/register")
async def register(
    form: RegisterRequest,
    auth_service: Annotated[AbstractAuthService, Depends(get_auth_service)],
) -> JSONResponse:
    try:
        token_set = await auth_service.register(
            form.email, form.username, form.password
        )
    except AbstractAuthService.EmailExists:
        raise HTTPException(400, "User with associated email already exist")
    except AbstractAuthService.UsernameExists:
        raise HTTPException(400, "User with associated username already exist")
    return response_from_set(token_set)
