from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from shared.dal.models.user import User
from shared.dal.repos.user import AbstractUserRepo
from api.di.jwt_service import get_jwt_service
from api.di.user_repo import get_user_repo
from api.services.jwt import AbstractJwtService


class UserWithEmailVerify(BaseModel):
    user: User
    email_verify_id: int


async def get_current_email_verification_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    jwt_service: Annotated[AbstractJwtService, Depends(get_jwt_service)],
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
) -> UserWithEmailVerify:
    obj = jwt_service.from_string(credentials.credentials)
    if obj is None:
        raise HTTPException(403, "Invalid bearer")
    if obj.ROLE_EMAIL_VERIFICATION not in obj.roles:
        raise HTTPException(403, "Invalid bearer")
    user = await user_repo.find_by_id(obj.user_id)
    if user is None:
        raise HTTPException(403, "User not found")
    return UserWithEmailVerify(user=user, email_verify_id=int(str(obj.email_verify)))
