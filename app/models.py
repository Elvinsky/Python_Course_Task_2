"""SQLAlchemy 2.0 declarative models. Provided: you do not need to change this file."""

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # float keeps the exercise simple; real money should use Decimal / Numeric(10, 2)
    price: Mapped[float]
    stock: Mapped[int] = mapped_column(default=0)
