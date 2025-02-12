from typing import Annotated

from fastapi import Depends
from api.di.settings import get_settings
from api.di.email_verification_repo import get_email_verification_repo
from shared.entities.email_verification import AbstractEmailVerificationRepo
from shared.entities.refresh_token import AbstractRefreshTokenRepo
from shared.entities.user import AbstractUserRepo
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
    email_verification_repo: Annotated[
        AbstractEmailVerificationRepo, Depends(get_email_verification_repo)
    ],
    jwt_service: Annotated[AbstractJwtService, Depends(get_jwt_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AbstractAuthService:
    return DefaultAuthService(
        user_repo, refresh_token_repo, email_verification_repo, jwt_service, settings
    )
