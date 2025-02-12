from shared.config.database import DatabaseConfig


config = DatabaseConfig.from_env()


def get_database_config() -> DatabaseConfig:
    return config
