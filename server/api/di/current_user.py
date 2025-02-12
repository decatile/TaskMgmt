from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.services.jwt.models import JwtRoles
from shared.entities.user import User
from shared.entities.user import ABCUserRepository
from api.di.jwt_service import get_jwt_service
from api.di.user_repo import get_user_repo
from api.services.jwt import AbstractJwtService


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    jwt_service: Annotated[AbstractJwtService, Depends(get_jwt_service)],
    user_repo: Annotated[ABCUserRepository, Depends(get_user_repo)],
) -> User:
    obj = jwt_service.from_string(credentials.credentials)
    if obj is None:
        raise HTTPException(403, "Invalid bearer")
    if JwtRoles.API not in obj.roles:
        raise HTTPException(403, "Invalid bearer")
    user = await user_repo.find(obj.user_id)
    if user is None:
        raise HTTPException(403, "User not found")
    return user
