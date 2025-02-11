from dataclasses import dataclass
from os import environ


@dataclass
class TokenConfig:
    access_token_expires_in: int
    refresh_token_expires_in: int

    @staticmethod
    def from_env() -> "TokenConfig":
        return TokenConfig(
            int(environ["ACCESS_TOKEN_EXPIRES_IN"]),
            int(environ["REFRESH_TOKEN_EXPIRES_IN"]),
        )
