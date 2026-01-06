from decimal import Decimal
from typing import Sequence

from sqlalchemy import func, select

from .connection import db_session
from .models import Category, Product


def get_all_categories() -> Sequence[Category]:
    stmt = select(Category).order_by(Category.name.asc())
    return db_session.scalars(stmt).all()


def get_category_by_id(category_id: int) -> Category | None:
    return db_session.get(Category, category_id)


def get_all_products() -> Sequence[Product]:
    stmt = select(Product).order_by(Product.name.asc())
    return db_session.scalars(stmt).all()


def get_product_by_id(product_id: int) -> Product | None:
    return db_session.get(Product, product_id)


def get_product_count_by_category(category_id: int) -> int:
    stmt = (
        select(func.count())
        .select_from(Product)
        .where(Product.category_id == category_id)
    )
    return db_session.scalar(stmt)


def add_category(name: str, description: str) -> None:
    category = Category(name=name, description=description)
    db_session.add(category)
    db_session.commit()


def add_product(
    name: str,
    description: str,
    price: Decimal,
    stock: int,
    category_id: int,
) -> None:
    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id,
    )
    db_session.add(product)
    db_session.commit()


def update_category(category_id: int, name: str, description: str) -> None:
    category = db_session.get(Category, category_id)
    if category:
        category.name = name
        category.description = description
        db_session.commit()


def update_product(
    product_id: int,
    name: str,
    description: str,
    price: Decimal,
    stock: int,
    category_id: int,
) -> None:
    product = db_session.get(Product, product_id)
    if product:
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.category_id = category_id
        db_session.commit()


def delete_category(category_id: int) -> None:
    category = db_session.get(Category, category_id)
    if category:
        db_session.delete(category)
        db_session.commit()


def delete_product(product_id: int) -> None:
    product = db_session.get(Product, product_id)
    if product:
        db_session.delete(product)
        db_session.commit()
