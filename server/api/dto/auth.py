from typing import Annotated
from fastapi import Response
from fastapi.responses import JSONResponse
from pydantic import AfterValidator, BaseModel
from email_validator import validate_email as validate_email_raw
from api.services.auth import AccessTokenSet, RefreshTokenSet
import re


def validate_email(value: str) -> str:
    try:
        validate_email_raw(value)
    except:  # noqa: E722
        raise ValueError("invalid email")
    return value


def validate_username(value: str) -> str:
    if len(value) > 64:
        raise ValueError("username must not be longer than 64 characters")
    if re.fullmatch(r"[a-z][a-z0-9_]*[a-z0-9]", value, re.I) is None:
        raise ValueError(
            "username must to start with letter, then continue with letters, digits or underscores and end with letter or digit"
        )
    return value


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("password must be longer than 7 characters")
    if len(value) > 64:
        raise ValueError("password must be shorter than 65 characters")
    return value


def validate_verification_code(value: str) -> str:
    if (len(value) != 4) or not re.fullmatch(r"\d{4}", value):
        raise ValueError("invalid verification code")
    return value


Email = Annotated[str, AfterValidator(validate_email)]
Username = Annotated[str, AfterValidator(validate_username)]
Password = Annotated[str, AfterValidator(validate_password)]
VerificationCode = Annotated[str, AfterValidator(validate_verification_code)]


class LoginRequest(BaseModel):
    email: Email
    password: Password


class RegisterRequest(BaseModel):
    email: Email
    username: Username
    password: Password


class VerifyRequest(BaseModel):
    code: VerificationCode


def response_with_refresh(response: Response, value: str, max_age: int) -> None:
    response.set_cookie(
        key="refresh_token",
        value=value,
        max_age=max_age,
        path="/auth/refresh",
        secure=True,
        httponly=True,
    )


def response_from_set(value: AccessTokenSet | RefreshTokenSet) -> JSONResponse:
    response = JSONResponse(
        {
            "access_token": value.access_token,
            "expires_in": value.access_token_expires_in,
            "scope": value.scope
        }
    )
    if isinstance(value, RefreshTokenSet):
        response_with_refresh(
            response, value.refresh_token, value.refresh_token_expires_in
        )
    return response
