from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import DoesNotExists
from src.models.schemas.products import Product
from src.views.interfaces.crud import CRUDInferface as ProductInterface
from src.models.dto.product import (
    ProductCreate, ProductUpdate
)
class ProductService(ProductInterface):
    
    async def get_element_by_id(self,session: AsyncSession, product_id:int):
        query = select(Product).where(Product.id == product_id)
        res = await session.execute(query)
        obj = res.scalar_one_or_none()
        if obj is None:
            raise DoesNotExists("Product not found")
        return obj
        
    
    async def create(self,  payload: ProductCreate, session: AsyncSession,):
        product = Product(
            **payload.model_dump()
        )
        session.add(product)
        await session.flush()
        await session.refresh(product)
        return product
    
    async def list(self, session: AsyncSession):
        query = select(Product).order_by(Product.id)
        result = await session.execute(query)
        return list(result.scalars().all())
    
    async def update(self, payload, product_id, session: AsyncSession):
        _object = await self.get_element_by_id(session=session, product_id=product_id)
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(_object, field, value)
        session.add(_object)
        await session.flush()
        await session.refresh(_object)
        return _object
    
    async def retrieve(self, product_id, session: AsyncSession):
        return await self.get_element_by_id(session=session, product_id=product_id) 
       
    async def delete(self, product_id, session):
        _object =  await self.get_element_by_id(session=session, product_id=product_id) 
        await session.delete(_object)
        await session.flush()