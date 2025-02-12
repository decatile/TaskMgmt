from os import environ
from pydantic import BaseModel


class TokenConfig(BaseModel):
    access_token_secret_key: str
    access_token_expires_in: int
    refresh_token_expires_in: int

    @staticmethod
    def from_env() -> "TokenConfig":
        return TokenConfig(
            access_token_secret_key=environ["ACCESS_TOKEN_SECRET_KEY"],
            access_token_expires_in=int(environ["ACCESS_TOKEN_EXPIRES_IN"]),
            refresh_token_expires_in=int(environ["REFRESH_TOKEN_EXPIRES_IN"]),
        )
