from src.models.dto.review import ReviewCreate, ReviewResponse, ReviewUpdate
from src.dependencies import get_review_service, get_session, get_current_user
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.schemas.user import User
from src.views.interfaces.crud import CRUDInferface
from src.core.utils import response

router = APIRouter(prefix="/reviews", )


@router.get("", response_model=list[ReviewResponse])
async def list_review(
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_review_service),
    session: AsyncSession = Depends(get_session),
) -> list[ReviewResponse]:
    return await response(func=repo.list, session=session)


@router.post("", response_model=ReviewResponse)
async def create_review(
    payload: ReviewCreate,
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_review_service),
    session: AsyncSession = Depends(get_session),
) -> ReviewResponse:
    return await response(func=repo.create, session=session, payload=payload)


@router.get("/{review_id}", response_model=ReviewResponse)
async def retrieve_review(
    review_id: int,
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_review_service),
    session: AsyncSession = Depends(get_session),
) -> ReviewResponse:
    return await response(func=repo.retrieve, review_id=review_id, session=session)


@router.patch("/{review_id}", response_model=ReviewResponse)
async def update_review(
    payload: ReviewUpdate,
    review_id: int,
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_review_service),
    session: AsyncSession = Depends(get_session),
) -> ReviewResponse:
    return await response(func=repo.update, review_id=review_id, session=session, payload=payload)

@router.delete("/{review_id}", status_code=204)
async def delete_review(
    review_id: int,
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_review_service),
    session: AsyncSession = Depends(get_session),
):
    await response(func=repo.delete, review_id=review_id, session=session)
