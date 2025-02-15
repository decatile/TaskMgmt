from shared.settings import Settings

s: Settings | None = None


def get_settings() -> Settings:
    global s
    if s is None:
        s = Settings() # type: ignore[call-arg]
    return s
