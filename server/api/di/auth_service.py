from typing import Annotated

from fastapi import Depends
from shared.dal.repos.refresh_token import AbstractRefreshTokenRepo
from shared.dal.repos.user import AbstractUserRepo
from api.di.jwt_service import get_jwt_service
from api.di.refresh_token_repo import get_refresh_token_repo
from api.di.user_repo import get_user_repo
from api.services.auth import AbstractAuthService, DefaultAuthService
from api.services.jwt import AbstractJwtService
from shared.config.token import TokenConfig
from api.di.token_config import get_token_config


def get_auth_service(
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
    refresh_token_repo: Annotated[
        AbstractRefreshTokenRepo, Depends(get_refresh_token_repo)
    ],
    jwt_service: Annotated[AbstractJwtService, Depends(get_jwt_service)],
    token_config: Annotated[TokenConfig, Depends(get_token_config)],
) -> AbstractAuthService:
    return DefaultAuthService(user_repo, refresh_token_repo, jwt_service, token_config)
