from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import DoesNotExists
from src.models.schemas.review import Review
from src.views.interfaces.crud import CRUDInferface as  ReviewInterface
from src.models.dto.review import ReviewUpdate, ReviewCreate


class ReviewService(ReviewInterface):
    async def get_element_by_id(self, session: AsyncSession, review_id: int):
        res = await session.execute(select(Review).where(Review.id == review_id))
        obj = res.scalar_one_or_none()
        if obj is None:
            raise DoesNotExists("Review not found")
        return obj

    async def create(self, payload: ReviewCreate, session: AsyncSession):
        review_obj = Review(**payload.model_dump())
        session.add(review_obj)
        await session.flush()
        await session.refresh(review_obj)
        return review_obj

    async def list(self, session: AsyncSession):
        query = select(Review).order_by(Review.id)
        result = await session.execute(query)
        return list(result.scalars().all())
    
    async def update(self, payload: ReviewUpdate, review_id: int, session: AsyncSession):
        _object = await self.get_element_by_id(session=session, review_id=review_id)
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(_object, field, value)
        session.add(_object)
        await session.flush()
        await session.refresh(_object)
        return _object
    
    async def retrieve(self, review_id, session: AsyncSession):
        return await self.get_element_by_id(session=session, review_id=review_id) 
       
    async def delete(self, review_id: int, session: AsyncSession):
        _object =  await self.get_element_by_id(session=session, review_id=review_id) 
        await session.delete(_object)
        await session.flush()