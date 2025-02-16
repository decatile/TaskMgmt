from typing import Annotated

from fastapi import Depends
from shared.settings import Settings
from api.di.settings import get_settings
from api.services.jwt import JwtService


def get_jwt_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> JwtService:
    return JwtService(settings)
