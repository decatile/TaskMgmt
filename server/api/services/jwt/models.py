from dataclasses import dataclass
from typing import ClassVar, List


@dataclass
class JwtObject:
    user_id: int
    roles: List[str]
    email_verify: int | None


class JwtRoles:
    API: ClassVar = "api"
    EMAIL_VERIFICATION: ClassVar = "email_verification"
