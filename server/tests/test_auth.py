from datetime import timedelta
from api.services.auth.service import AuthService
from shared.entities.email_verification.model import EmailVerification
from shared.entities.refresh_token.model import RefreshToken
from shared.utils import utc_now, hash_password
from shared.entities.user.model import User
from shared.settings import Settings
from shared.entities.user import UserRepository
from shared.entities.refresh_token import RefreshTokenRepository
from shared.entities.email_verification import EmailVerificationRepository
from api.services.jwt import JwtService
from pytest_mock import MockFixture
import pytest


@pytest.mark.asyncio
async def test_auth(mocker: MockFixture):
    user_repo = mocker.AsyncMock(UserRepository)
    token_repo = mocker.AsyncMock(RefreshTokenRepository)
    email_repo = mocker.AsyncMock(EmailVerificationRepository)
    jwt_service = mocker.AsyncMock(JwtService)
    settings = mocker.PropertyMock(Settings)
    service = AuthService(user_repo, token_repo, email_repo, jwt_service, settings)

    # User not found
    user_repo.find_by_email.return_value = None
    with pytest.raises(AuthService.UserNotFound):
        await service.login("", "")

    # Invalid password
    user_repo.find_by_email.return_value = User(password_hash=hash_password("1"))
    with pytest.raises(AuthService.InvalidPassword):
        await service.login("", "")

    # Email exists
    user_repo.lookup_by_email_or_username.return_value = "email"
    with pytest.raises(AuthService.EmailExists):
        await service.register("", "", "")

    # Username exists
    user_repo.lookup_by_email_or_username.return_value = "username"
    with pytest.raises(AuthService.UsernameExists):
        await service.register("", "", "")

    # Refresh token not found
    token_repo.find.return_value = None
    with pytest.raises(AuthService.InvalidRefreshToken):
        await service.refresh("")

    # Refresh token expired
    token_repo.find.return_value = RefreshToken(
        created_at=utc_now() - timedelta(days=365)
    )
    settings.refresh_token_expires_in = 0
    with pytest.raises(AuthService.InvalidRefreshToken):
        await service.refresh("")

    # Invalid verify
    email_repo.find.return_value = None
    with pytest.raises(AuthService.InvalidVerifyId):
        await service.verify(1, 1, "")

    # Invalid code
    email_repo.find.return_value = EmailVerification(code="")
    with pytest.raises(AuthService.InvalidCode):
        await service.verify(1, 1, '1')
