from pydantic_settings import BaseSettings


class RuntimeSettings(BaseSettings):
    gen_docs: bool = False
