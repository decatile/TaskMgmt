from typing import Any, Dict, Literal
from fastapi import HTTPException

ErrorCode = Literal[
    "access_token_not_present",
    "access_token_invalid",
    "access_token_forbidden",
    "access_token_poisoned",
    "user_not_found",
    "user_already_exist",
    "invalid_password",
    "invalid_request_id",
    "invalid_code",
    "refresh_token_invalid",
]

error_code_to_status: Dict[ErrorCode, int] = {
    "access_token_not_present": 401,
    "access_token_invalid": 401,
    "access_token_forbidden": 403,
    "access_token_poisoned": 401,
    "user_not_found": 400,
    "user_already_exist": 400,
    "invalid_password": 400,
    "invalid_request_id": 400,
    "invalid_code": 401,
    "refresh_token_invalid": 401,
}


class DetailedHTTPException(HTTPException):
    def __init__(
        self,
        code: ErrorCode,
        **extension: Any,
    ):
        super().__init__(
            error_code_to_status[code],
            {"code": code, **extension},
        )
