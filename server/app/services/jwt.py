from abc import ABC, abstractmethod
from datetime import datetime
import jwt
from pydantic import BaseModel

from app.config.token import TokenConfig


class JwtString(BaseModel):
    string: str
    expires_in: int


class JwtObject(BaseModel):
    user_id: int


class AbstractJwtService(ABC):
    @abstractmethod
    def new(self, user_id: int) -> JwtString: ...

    @abstractmethod
    def from_string(self, value: str) -> JwtObject | None: ...


class DefaultJwtService(AbstractJwtService):
    def __init__(self, config: TokenConfig):
        super().__init__()
        self.config = config

    def new(self, user_id: int) -> JwtString:
        now = int(datetime.now().timestamp())
        return JwtString(
            string=jwt.encode(
                {
                    "sub": str(user_id),
                    "iat": now,
                    "exp": now + self.config.access_token_expires_in,
                },
                self.config.access_token_secret_key,
                "HS256",
            ),
            expires_in=self.config.access_token_expires_in,
        )

    def from_string(self, value: str) -> JwtObject | None:
        try:
            obj = jwt.decode(
                value,
                self.config.access_token_secret_key,
                ["HS256"],
                verify=True,
            )
            return JwtObject(user_id=int(obj["sub"]))
        except:  # noqa: E722
            return None
