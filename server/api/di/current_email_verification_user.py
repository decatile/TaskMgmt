from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dataclasses import dataclass
from api.services.jwt.models import JwtRoles
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
        raise HTTPException(401, "No access token passed")
    obj = jwt_service.from_string(credentials.credentials)
    if obj is None:
        raise HTTPException(401, "Invalid access token")
    if JwtRoles.EMAIL_VERIFICATION not in obj.roles:
        raise HTTPException(403, "Access token not allowed to verify email")
    user = await user_repo.find(obj.user_id)
    if user is None:
        raise HTTPException(401, "User associated with access token not found")
    return UserWithEmailVerify(user=user, email_verify_id=int(str(obj.email_verify)))
