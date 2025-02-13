from typing import Annotated

from fastapi import Depends
from api.di.settings import get_settings
from api.di.email_verification_repo import get_email_verification_repo
from shared.entities.user import UserRepository
from shared.entities.email_verification import EmailVerificationRepository
from shared.entities.refresh_token import RefreshTokenRepository
from api.di.jwt_service import get_jwt_service
from api.di.refresh_token_repo import get_refresh_token_repo
from api.di.user_repo import get_user_repo
from api.services.auth import AuthService
from api.services.jwt import JwtService
from shared.settings import Settings


def get_auth_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    refresh_token_repo: Annotated[
        RefreshTokenRepository, Depends(get_refresh_token_repo)
    ],
    email_verification_repo: Annotated[
        EmailVerificationRepository, Depends(get_email_verification_repo)
    ],
    jwt_service: Annotated[JwtService, Depends(get_jwt_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthService:
    return AuthService(
        user_repo, refresh_token_repo, email_verification_repo, jwt_service, settings
    )
