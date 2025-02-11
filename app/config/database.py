from dataclasses import dataclass
from os import environ


@dataclass
class DatabaseConfig:
    url: str

    @staticmethod
    def from_env() -> "DatabaseConfig":
        return DatabaseConfig(environ["DATABASE_URL"])
