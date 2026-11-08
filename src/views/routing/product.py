from src.models.dto.product import ProductCreate, ProductResponse, ProductUpdate
from src.dependencies import get_product_service, get_session, get_current_user
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.schemas.user import User
from src.views.interfaces.crud import CRUDInferface
from src.core.utils import response

router = APIRouter(prefix="/products")


@router.get("", response_model=list[ProductResponse])
async def list_product(
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_product_service),
    session: AsyncSession = Depends(get_session),
) -> list[ProductResponse]:
    return await response(func=repo.list, session=session)


@router.post("", response_model=ProductResponse)
async def create_product(
    payload: ProductCreate,
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_product_service),
    session: AsyncSession = Depends(get_session),
) -> ProductResponse:
    return await response(func=repo.create, session=session, payload=payload)


@router.get("/{product_id}", response_model=ProductResponse)
async def retrieve_product(
    product_id:int,
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_product_service),
    session: AsyncSession = Depends(get_session),
) -> ProductResponse:
    return await response(func=repo.retrieve, product_id=product_id, session=session)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    payload: ProductUpdate,
    product_id:int,
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_product_service),
    session: AsyncSession = Depends(get_session),
) -> ProductResponse:
    return await response(func=repo.update, product_id=product_id, session=session, payload=payload)

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id:int,
    _: User = Depends(get_current_user),
    repo: CRUDInferface = Depends(get_product_service),
    session: AsyncSession = Depends(get_session),
):
    await response(func=repo.delete, product_id=product_id, session=session)
