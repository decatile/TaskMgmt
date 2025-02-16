from datetime import datetime
from shared.settings import Settings
from .models import JwtObject
import jwt


class JwtService:
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    def new(self, user_id: int) -> str:
        now = int(datetime.now().timestamp())
        obj = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + self.settings.access_token_expires_in,
        }
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
            )
        except:  # noqa: E722[]
            return None
