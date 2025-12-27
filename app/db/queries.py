from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from .connection import engine
from .models import Category, Product

Session = sessionmaker(bind=engine)


def get_all_categories():
    session = Session()
    stmt = select(Category).order_by(Category.name.asc())
    return session.scalars(stmt).all()


def get_category_by_id(category_id):
    session = Session()
    stmt = select(Category).where(Category.id == category_id)
    return session.scalars(stmt).first()


def get_all_products():
    session = Session()
    stmt = select(Product).order_by(Product.name.asc())
    return session.scalars(stmt).all()


def get_product_by_id(product_id):
    session = Session()
    return session.get(Product, product_id)


def get_products_by_category(category_id):
    session = Session()
    stmt = (
        select(Product)
        .where(Product.category_id == category_id)
        .order_by(Product.name.asc())
    )
    return session.scalars(stmt).all()


def add_category(name, description):
    session = Session()
    category = Category(name=name, description=description)
    session.add(category)
    session.commit()


def add_product(name, description, price, stock, category_id):
    session = Session()
    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id,
    )
    session.add(product)
    session.commit()


def update_category(category_id, name, description):
    session = Session()
    category = session.get(Category, category_id)
    if category:
        category.name = name
        category.description = description
        session.commit()


def update_product(product_id, name, description, price, stock, category_id):
    session = Session()
    product = session.get(Product, product_id)
    if product:
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.category_id = category_id
        session.commit()


def delete_category(category_id):
    session = Session()
    category = session.get(Category, category_id)
    if category:
        session.delete(category)
        session.commit()


def delete_product(product_id):
    session = Session()
    product = session.get(Product, product_id)
    if product:
        session.delete(product)
        session.commit()
