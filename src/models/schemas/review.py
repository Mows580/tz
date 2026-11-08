from sqlalchemy import Integer, String, Text, ForeignKey
from src.models.schemas.base import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Review(Model):
    product_id: Mapped[int] = mapped_column(
        ForeignKey(column="products.id", ondelete="CASCADE"), nullable=False
    )
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str | None] = mapped_column(Text, nullable=True)


    product: Mapped["Product"] = relationship(
        "Product", back_populates='reviews'
    )