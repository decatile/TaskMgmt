from typing import Annotated

from fastapi import Depends
from app.dal.repos.refresh_token import AbstractRefreshTokenRepo
from app.dal.repos.user import AbstractUserRepo
from app.di.jwt_service import get_jwt_service
from app.di.refresh_token_repo import get_refresh_token_repo
from app.di.user_repo import get_user_repo
from app.services.auth import AbstractAuthService, DefaultAuthService
from app.services.jwt import AbstractJwtService


def get_auth_service(
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
    refresh_token_repo: Annotated[
        AbstractRefreshTokenRepo, Depends(get_refresh_token_repo)
    ],
    jwt_service: Annotated[AbstractJwtService, Depends(get_jwt_service)],
) -> AbstractAuthService:
    return DefaultAuthService(user_repo, refresh_token_repo, jwt_service)
