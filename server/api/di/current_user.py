from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.services.jwt.models import JwtScope
from api.dto.base import DetailedHTTPException
from shared.entities.user import User
from shared.entities.user import UserRepository
from api.di.jwt_service import get_jwt_service
from api.di.user_repo import get_user_repo
from api.services.jwt import JwtService


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))
    ],
    jwt_service: Annotated[JwtService, Depends(get_jwt_service)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> User:
    if credentials is None:
        raise DetailedHTTPException("access_token_not_present")
    obj = jwt_service.from_string(credentials.credentials)
    if obj is None:
        raise DetailedHTTPException("access_token_invalid")
    if JwtScope.API != obj.scope:
        raise DetailedHTTPException("access_token_forbidden", resource="API")
    user = await user_repo.find_enabled(obj.user_id)
    if user is None:
        raise DetailedHTTPException("access_token_poisoned")
    return user
