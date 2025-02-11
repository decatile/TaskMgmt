from typing import Annotated
from pydantic import AfterValidator, BaseModel
import re
from email_validator import validate_email as validate_email_raw


def validate_email(value: str) -> str:
    try:
        validate_email_raw(value)
    except:  # noqa: E722
        raise ValueError("Invalid email")
    return value


def validate_username(value: str) -> str:
    if len(value) > 64:
        raise ValueError("Username must not be longer than 64 characters")
    if re.fullmatch(r"[a-z][a-z0-9_]*[a-z0-9]", value, re.I) is None:
        raise ValueError(
            "Username must to start with letter, then continue with letters, digits or underscores and end with letter or digit"
        )
    return value


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be longer than 7 characters")
    if len(value) > 64:
        raise ValueError("Password must be shorter than 65 characters")
    return value


Email = Annotated[str, AfterValidator(validate_email)]
Username = Annotated[str, AfterValidator(validate_username)]
Password = Annotated[str, AfterValidator(validate_password)]


class LoginRequest(BaseModel):
    username: Username
    password: Password


class RegisterRequest(BaseModel):
    email: Email
    username: Username
    password: Password
