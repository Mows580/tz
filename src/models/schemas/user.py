from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.models.schemas.base import Model

class User(Model):
    username: Mapped[str] = mapped_column(
        String(255), unique=True,nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),nullable=False
    )