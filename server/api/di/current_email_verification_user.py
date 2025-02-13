from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dataclasses import dataclass
from api.services.jwt.models import JwtScope
from api.dto.base import DetailedHTTPException
from shared.entities.user import User
from shared.entities.user import ABCUserRepository
from api.di.jwt_service import get_jwt_service
from api.di.user_repo import get_user_repo
from api.services.jwt import AbstractJwtService


@dataclass
class UserWithEmailVerify:
    user: User
    email_verify_id: int


async def get_current_email_verification_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))
    ],
    jwt_service: Annotated[AbstractJwtService, Depends(get_jwt_service)],
    user_repo: Annotated[ABCUserRepository, Depends(get_user_repo)],
) -> UserWithEmailVerify:
    if credentials is None:
        raise DetailedHTTPException("access_token_not_present")
    obj = jwt_service.from_string(credentials.credentials)
    if obj is None:
        raise DetailedHTTPException("access_token_invalid")
    if JwtScope.EMAIL_VERIFICATION != obj.scope:
        raise DetailedHTTPException(
            "access_token_forbidden", resource="EMAIL_VERIFICATION"
        )
    user = await user_repo.find(obj.user_id)
    if user is None:
        raise DetailedHTTPException("access_token_poisoned")
    return UserWithEmailVerify(user=user, email_verify_id=int(str(obj.email_verify)))
