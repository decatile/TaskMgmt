from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    allow_origins: str
    database_url: str
    redis_url: str
    access_token_secret_key: str
    access_token_expires_in: int
    refresh_token_expires_in: int
    email_verification_enable: bool
    email_verification_code_expires_in: int

