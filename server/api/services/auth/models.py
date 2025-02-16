from pydantic import BaseModel


class TokenSet(BaseModel):
    access_token: str
    access_token_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int


class VerificationRequestId(BaseModel):
    request_id: str
