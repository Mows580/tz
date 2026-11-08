from pydantic import BaseModel, PlainSerializer
from datetime import datetime
from typing import Annotated, Optional

DateTime = Annotated[
    datetime,
    PlainSerializer(lambda value: value.strftime("%Y-%m-%d"), return_type=str)
]

class ReviewBase(BaseModel):
    product_id: int
    author: str
    rating: int
    text: Optional[str] = None
    
    
class ReviewCreate(ReviewBase): ...

class ReviewUpdate(BaseModel):
    product_id: Optional[int] = None
    author: Optional[str] = None
    rating: Optional[int] = None
    text: Optional[str] = None
    
    
class ReviewResponse(ReviewBase):
    id:int
    created_at: DateTime
    
    