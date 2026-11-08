from pydantic import BaseModel, Field, PlainSerializer
from typing import Optional
from uuid import uuid4
from typing import Annotated
from  datetime import datetime

DateTime = Annotated[
    datetime,
    PlainSerializer(
        lambda v: v.strftime("%Y-%m-%d"), return_type=str
    )
]

class ProductBase(BaseModel):
    name: str
    description:str
    price:float = Field(default=100, ge=0,le=100000000)
    
class ProductCreate(ProductBase): ...

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description:Optional[str] = None
    price:Optional[float] = Field(default=100, ge=0,le=100000000)
    
    
class ProductResponse(ProductBase):
    id:int
    created_at: DateTime