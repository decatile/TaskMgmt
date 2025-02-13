from dataclasses import dataclass
from typing import ClassVar


@dataclass
class JwtObject:
    user_id: int
    scope: str
    email_verify: int | None


class JwtScope:
    API: ClassVar = "api"
    EMAIL_VERIFICATION: ClassVar = "email_verification"
