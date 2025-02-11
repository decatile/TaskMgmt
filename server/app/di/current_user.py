from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.dal.models.user import User
from app.dal.repos.user import AbstractUserRepo
from app.di.jwt_service import get_jwt_service
from app.di.user_repo import get_user_repo
from app.services.jwt import AbstractJwtService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_service: Annotated[AbstractJwtService, Depends(get_jwt_service)],
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
) -> User:
    obj = jwt_service.from_string(token)
    if obj is None:
        raise HTTPException(401, "Invalid bearer")
    user = await user_repo.find_by_id(obj.user_id)
    if user is None:
        raise HTTPException(401, "User not found")
    return user
