from typing import Annotated
from fastapi.responses import JSONResponse
from pydantic import AfterValidator, BaseModel
from email_validator import validate_email as validate_email_raw
from app.services.auth import TokenSet
import re


def validate_email(value: str) -> str:
    try:
        validate_email_raw(value)
    except Exception as e:  # noqa: E722
        print(e)
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


Email = Annotated[str, AfterValidator(validate_email)]
Username = Annotated[str, AfterValidator(validate_username)]
Password = Annotated[str, AfterValidator(validate_password)]


class LoginRequest(BaseModel):
    email: Email
    password: Password


class RegisterRequest(BaseModel):
    email: Email
    username: Username
    password: Password


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int


def response_from_set(value: TokenSet) -> JSONResponse:
    return JSONResponse(
        {
            "access_token": value.access_token,
            "expires_in": value.access_token_expires_in,
        },
        headers={
            "Set-Cookie": f"refresh_token={value.refresh_token};max-age={value.refresh_token_expires_in};path=/auth/refresh"
        },
    )
