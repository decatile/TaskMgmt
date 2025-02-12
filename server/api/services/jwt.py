from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from pydantic import BaseModel
from shared.settings import Settings
import jwt


class JwtObject(BaseModel):
    user_id: int
    roles: List[str]
    email_verify: int | None

    ROLE_API = "api"
    ROLE_EMAIL_VERIFICATION = "email_verify"


class AbstractJwtService(ABC):
    @abstractmethod
    def new(
        self, user_id: int, roles: List[str], email_verification_id: int | None = None
    ) -> str: ...

    @abstractmethod
    def from_string(self, value: str) -> JwtObject | None: ...


class DefaultJwtService(AbstractJwtService):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    def new(
        self, user_id: int, roles: List[str], email_verification_id: int | None = None
    ) -> str:
        now = int(datetime.now().timestamp())
        obj = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + self.settings.access_token_expires_in,
            "roles": roles,
        }
        if email_verification_id is not None:
            obj["email_verify"] = email_verification_id
        return jwt.encode(
            obj,
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
            return JwtObject(
                user_id=int(obj["sub"]),
                roles=obj["roles"],
                email_verify=obj.get("email_verify"),
            )
        except:  # noqa: E722[]
            return None
