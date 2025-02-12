from shared.config.token import TokenConfig


config = TokenConfig.from_env()


def get_token_config() -> TokenConfig:
    return config
