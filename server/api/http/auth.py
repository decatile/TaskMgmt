from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from api.di.auth_service import get_auth_service
from api.dto.auth import (
    LoginRequest,
    RegisterRequest,
    VerifyRequest,
    response_from_set,
    response_with_refresh,
)
from api.services.auth import AbstractAuthService
from api.di.current_email_verification_user import (
    UserWithEmailVerify,
    get_current_email_verification_user,
)


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


@auth_router.post("/verify")
async def verify(
    creds: Annotated[UserWithEmailVerify, Depends(get_current_email_verification_user)],
    auth_service: Annotated[AbstractAuthService, Depends(get_auth_service)],
    code: VerifyRequest,
):
    try:
        token_set = await auth_service.verify(
            creds.user.id, creds.email_verify_id, code=code.code
        )
    except AbstractAuthService.InvalidVerifyId:
        raise HTTPException(401, "Verification associated with access token not found")
    except AbstractAuthService.InvalidCode:
        raise HTTPException(400, "Invalid code")
    return response_from_set(token_set)


@auth_router.get("/refresh/roll")
async def refresh(
    refresh_token: Annotated[str, Cookie()],
    auth_service: Annotated[AbstractAuthService, Depends(get_auth_service)],
) -> JSONResponse:
    try:
        token_set = await auth_service.refresh(refresh_token)
    except AbstractAuthService.InvalidRefreshToken:
        raise HTTPException(
            401,
            "Invalid refresh token",
        )
    return response_from_set(token_set)


@auth_router.get("/refresh/logout")
async def logout(
    refresh_token: Annotated[str, Cookie()],
    auth_service: Annotated[AbstractAuthService, Depends(get_auth_service)],
) -> Response:
    await auth_service.logout(refresh_token)
    response = JSONResponse({"logout": 1})
    response_with_refresh(response, refresh_token, -1)
    return response
