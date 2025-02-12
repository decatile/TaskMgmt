from shared.config.redis import RedisConfig


config = RedisConfig.from_env()


def get_redis_config() -> RedisConfig:
    return config
