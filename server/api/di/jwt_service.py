from typing import Annotated

from fastapi import Depends
from shared.config.token import TokenConfig
from api.di.token_config import get_token_config
from api.services.jwt import AbstractJwtService, DefaultJwtService


def get_jwt_service(
    config: Annotated[TokenConfig, Depends(get_token_config)],
) -> AbstractJwtService:
    return DefaultJwtService(config)
