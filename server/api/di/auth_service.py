from typing import Annotated

from fastapi import Depends
from api.di.settings import get_settings
from shared.dal.repos.refresh_token import AbstractRefreshTokenRepo
from shared.dal.repos.user import AbstractUserRepo
from api.di.jwt_service import get_jwt_service
from api.di.refresh_token_repo import get_refresh_token_repo
from api.di.user_repo import get_user_repo
from api.services.auth import AbstractAuthService, DefaultAuthService
from api.services.jwt import AbstractJwtService
from shared.settings import Settings


def get_auth_service(
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
    refresh_token_repo: Annotated[
        AbstractRefreshTokenRepo, Depends(get_refresh_token_repo)
    ],
    jwt_service: Annotated[AbstractJwtService, Depends(get_jwt_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AbstractAuthService:
    return DefaultAuthService(user_repo, refresh_token_repo, jwt_service, settings)
