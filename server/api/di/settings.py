from shared.settings import Settings

s = Settings() # type: ignore[call-arg]


def get_settings() -> Settings:
    return s
