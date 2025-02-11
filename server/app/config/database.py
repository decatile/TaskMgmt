from os import environ
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    url: str

    @staticmethod
    def from_env() -> "DatabaseConfig":
        return DatabaseConfig(url=environ["DATABASE_URL"])
