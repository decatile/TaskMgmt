from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.dal.repos.refresh_token import AbstractRefreshTokenRepo
from app.dal.repos.user import AbstractUserRepo
from app.di.refresh_token_repo import get_refresh_token_repo
from app.di.user_repo import get_user_repo
from app.utils.hash import hash_password


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    access_token_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int


auth_router = APIRouter()


@auth_router.post("/login")
async def login(
    form: LoginRequest,
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
    refresh_token_repo: Annotated[
        AbstractRefreshTokenRepo, Depends(get_refresh_token_repo)
    ],
) -> TokenResponse:
    user = await user_repo.find_by_username(form.username)
    if user is None:
        raise HTTPException(400, "User not found")
    if user.password_hash != hash_password(form.password):
        raise HTTPException(400, "Invalid password")
    _token = await refresh_token_repo.new(user.id)
    raise NotImplementedError
