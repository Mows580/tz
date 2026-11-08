from src.models.dto.user import UserCreate, UserLogin, UserResponse
from fastapi import APIRouter, Depends, status
from src.dependencies import get_session,get_auth_service
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.schemas.user import User
from src.views.interfaces.auth import AuthInterface
from src.core.utils import response


router = APIRouter(
    prefix='/auth'
)

@router.post('/login', response_model=UserResponse)
async def login(
    payload: UserLogin,
    session: AsyncSession = Depends(get_session),
    repo: AuthInterface = Depends(get_auth_service)
):
    return await response(
        func=repo.login,
        payload=payload,
        session=session
    )



@router.post('/register')
async def register(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
    repo: AuthInterface = Depends(get_auth_service)
):
    return await response(
        func=repo.registration,
        payload=payload,
        session=session
    )
