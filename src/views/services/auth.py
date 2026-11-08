from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import(
    hash_password,verify_password,create_access_token
)
from src.models.schemas.user import User
from src.core.exceptions import DoesNotExists, UniqueConstraint
from src.models.dto.user import (
    UserCreate, UserLogin
)
from src.views.interfaces.auth import AuthInterface


class AuthService(AuthInterface):
    
    async def login(self, payload:UserLogin, session:AsyncSession):
        res = await session.execute(
            select(User).where(User.username == payload.username)
            )
        user = res.scalar_one_or_none()
        if not user or not verify_password(payload.password, user.hashed_password):
            raise DoesNotExists(
                "User with such credentials does not exist"
            )
        token = create_access_token(subject=user.id, extra={"username": user.username})
        return {
            'access_token': token,
            'user_id': user.id
        }

    async def registration(self, payload:UserCreate, session:AsyncSession):
        res = await session.execute(
            select(User).where(User.username == payload.username)
        )
        if res.scalar_one_or_none():
            raise UniqueConstraint(
                "User with this username already exists"
            )
        user = User(
            username=payload.username,
            hashed_password=hash_password(payload.password)
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)
        token = create_access_token(subject=user.id, extra={"username": user.username})
        return {
            'access_token': token,
            'user_id': user.id
        }