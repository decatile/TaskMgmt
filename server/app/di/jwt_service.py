from typing import Annotated

from fastapi import Depends
from app.config.token import TokenConfig
from app.di.token_config import get_token_config
from app.services.jwt import AbstractJwtService, DefaultJwtService


def get_jwt_service(
    config: Annotated[TokenConfig, Depends(get_token_config)],
) -> AbstractJwtService:
    return DefaultJwtService(config)
