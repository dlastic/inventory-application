from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import Config


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r}, description={self.description!r})"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="SET DEFAULT"),
        server_default=str(Config.DEFAULT_CATEGORY_ID),
        default=Config.DEFAULT_CATEGORY_ID,
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    category: Mapped[Category] = relationship(back_populates="products")

    def __repr__(self) -> str:
        return (
            f"Product(id={self.id!r}, name={self.name!r}, description={self.description!r}, "
            f"price={self.price!r}, stock={self.stock!r}, category_id={self.category_id!r})"
        )
