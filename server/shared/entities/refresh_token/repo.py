from sqlalchemy.ext.asyncio import AsyncSession
from shared.abc import Repository
from shared.entities.refresh_token import RefreshToken


class RefreshTokenRepository(Repository[RefreshToken, str]):
    def __init__(self, session: AsyncSession):
        super().__init__(
            RefreshToken,
            session,
        )

    def new(self, user_id: int) -> RefreshToken:
        return RefreshToken(user_id=user_id)
