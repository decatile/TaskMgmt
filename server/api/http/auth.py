from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.responses import JSONResponse
from api.di.auth_service import get_auth_service
from api.dto.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    VerifyRequest,
    response_from_set,
    response_with_refresh,
)
from api.services.auth import AuthService
from api.dto.base import DetailedHTTPException


auth_router = APIRouter()


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    description='''
    Retrieve token set using email and password.
    
    Possible errors:
    If user not found:
        400 "user_not_found"
    If password is invalid:
        400 "invalid_password"''',
)
async def login(
    form: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        token_set = await auth_service.login(form.email, form.password)
    except AuthService.UserNotFound:
        raise DetailedHTTPException("user_not_found")
    except AuthService.InvalidPassword:
        raise DetailedHTTPException("invalid_password")
    return response_from_set(token_set)


@auth_router.post(
    "/register",
    response_model=TokenResponse,
    description='''
    Register user by username, email and password. If email authentication enabled, returns a special access token for verification.
    
    Possible errors:
    If user already exist:
        400 "user_already_exist", cause: "email" | "username"''',
)
async def register(
    form: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> JSONResponse:
    try:
        token_set = await auth_service.register(
            form.email, form.username, form.password
        )
    except AuthService.EmailExists:
        raise DetailedHTTPException("user_already_exist", cause="email")
    except AuthService.UsernameExists:
        raise DetailedHTTPException("user_already_exist", cause="username")
    return response_from_set(token_set)


@auth_router.post(
    "/verify",
    response_model=TokenResponse,
    description='''
    Verify email by special access token and code
    
    Possible errors:
    If request_id is invalid
        400 "invalid_request_id"
    If code is invalid:
        401 "invalid_code"''',
)
async def verify(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    request: VerifyRequest,
):
    try:
        token_set = await auth_service.verify(
            request_id=request.request_id, code=request.code
        )
    except AuthService.InvalidRequestId:
        raise DetailedHTTPException("invalid_request_id")
    except AuthService.InvalidCode:
        raise DetailedHTTPException("invalid_code")
    return response_from_set(token_set)


@auth_router.get(
    "/refresh/roll",
    response_model=TokenResponse,
    description="""
    Rotate new refresh token
    
    Possible errors:
    If refresh token is invalid:
        401 "refresh_token_invalid"
    """,
)
async def refresh(
    refresh_token: Annotated[str, Cookie()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> JSONResponse:
    try:
        token_set = await auth_service.refresh(refresh_token)
    except AuthService.InvalidRefreshToken:
        raise DetailedHTTPException("refresh_token_invalid")
    return response_from_set(token_set)


@auth_router.get(
    "/refresh/logout",
    description="""
    Logout by refresh token, returns empty string""",
)
async def logout(
    refresh_token: Annotated[str, Cookie()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Response:
    await auth_service.logout(refresh_token)
    response = Response()
    response_with_refresh(response, refresh_token, -1)
    return response
