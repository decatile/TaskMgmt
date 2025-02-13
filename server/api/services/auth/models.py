from pydantic import BaseModel


class AccessTokenSet(BaseModel):
    scope: str
    access_token: str
    access_token_expires_in: int


class RefreshTokenSet(AccessTokenSet):
    refresh_token: str
    refresh_token_expires_in: int
