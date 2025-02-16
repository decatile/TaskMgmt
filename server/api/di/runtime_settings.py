from ..settings import RuntimeSettings

s: RuntimeSettings | None = None


def get_runtime_settings() -> RuntimeSettings:
    global s
    if s is None:
        s = RuntimeSettings()  # type: ignore[call-arg]
    return s
