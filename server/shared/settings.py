from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    access_token_secret_key: str
    access_token_expires_in: int
    refresh_token_expires_in: int


settings = Settings()  # type: ignore[call-arg]
