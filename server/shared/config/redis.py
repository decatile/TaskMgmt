from os import environ
from pydantic import BaseModel


class RedisConfig(BaseModel):
    url: str

    @staticmethod
    def from_env() -> "RedisConfig":
        return RedisConfig(url=environ["REDIS_URL"])
