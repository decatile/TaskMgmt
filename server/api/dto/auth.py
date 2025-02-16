from typing import Annotated
from fastapi import Response
from fastapi.responses import JSONResponse
from pydantic import AfterValidator, BaseModel
from email_validator import validate_email as validate_email_raw
from api.services.auth import TokenSet
import re


def validate_email(value: str) -> str:
    try:
        validate_email_raw(value)
    except:  # noqa: E722
        raise ValueError("invalid email")
    return value


def validate_username(value: str) -> str:
    if len(value) < 5:
        raise ValueError("username should contain at least 5 characters")
    if len(value) > 32:
        raise ValueError("username should contain at most 32 characters")
    if not re.fullmatch(r"[a-z0-8-]+", value, re.I):
        raise ValueError(
            "username should contain only Latin letters, numbers and hyphens"
        )
    if re.match(r"^-|-$", value):
        raise ValueError("username shouldn't begin or end with hyphen")
    if "--" in value:
        raise ValueError("username shouldn't contain two hyphens in a row")
    return value


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("password should contain at least 8 characters")
    if len(value) > 64:
        raise ValueError("password should contain at most 64 characters")
    if not any(1 for i in value if i.isalpha()):
        raise ValueError("password should contain at least one letter")
    if not any(1 for i in value if i.isdigit()):
        raise ValueError("password should contain at least one digit")
    if " " in value:
        raise ValueError("password should not contain space")
    return value


def validate_verification_code(value: str) -> str:
    if (len(value) != 4) or not all(1 for i in value if i.isdigit()):
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
    request_id: str
    code: VerificationCode


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int


def response_with_refresh(response: Response, value: str, max_age: int) -> None:
    response.set_cookie(
        key="refresh_token",
        value=value,
        max_age=max_age,
        path="/auth/refresh",
        secure=True,
        httponly=True,
    )


def response_from_set(value: TokenSet) -> JSONResponse:
    response = JSONResponse(
        {
            "access_token": value.access_token,
            "expires_in": value.access_token_expires_in,
        }
    )
    response_with_refresh(response, value.refresh_token, value.refresh_token_expires_in)
    return response
