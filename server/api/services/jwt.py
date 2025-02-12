from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel
from shared.settings import Settings
import jwt


class JwtString(BaseModel):
    string: str
    expires_in: int


class JwtObject(BaseModel):
    user_id: int


class AbstractJwtService(ABC):
    @abstractmethod
    def new(self, user_id: int) -> str: ...

    @abstractmethod
    def from_string(self, value: str) -> JwtObject | None: ...


class DefaultJwtService(AbstractJwtService):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    def new(self, user_id: int) -> str:
        now = int(datetime.now().timestamp())
        return jwt.encode(
            {
                "sub": str(user_id),
                "iat": now,
                "exp": now + self.settings.access_token_expires_in,
            },
            self.settings.access_token_secret_key,
            "HS256",
        )

    def from_string(self, value: str) -> JwtObject | None:
        try:
            obj = jwt.decode(
                value,
                self.settings.access_token_secret_key,
                ["HS256"],
                verify=True,
            )
            return JwtObject(user_id=int(obj["sub"]))
        except:  # noqa: E722
            return None
