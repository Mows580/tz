from sqlalchemy import DateTime, Numeric, String, Text
from src.models.schemas.base import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Product(Model):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="product", cascade="all, delete-orphan"
    )
    
