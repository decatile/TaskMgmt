from typing import Annotated
from fastapi import APIRouter, Depends
from app.dal.models.user import User
from app.di.current_user import get_current_user
from app.dto.profile import ProfileResponse


profile_router = APIRouter()


@profile_router.post("/me")
async def me(user: Annotated[User, Depends(get_current_user)]) -> ProfileResponse:
    return ProfileResponse(
        email=user.email, username=user.username, registered_at=user.created_at
    )
