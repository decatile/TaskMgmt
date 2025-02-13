from typing import Annotated
from fastapi import APIRouter, Depends
from shared.entities.user import User
from api.di.current_user import get_current_user
from api.dto.profile import ProfileResponse


profile_router = APIRouter()


@profile_router.get("/me")
async def me(user: Annotated[User, Depends(get_current_user)]) -> ProfileResponse:
    return ProfileResponse(
        email=user.email, username=user.username, registered_at=user.created_at
    )
