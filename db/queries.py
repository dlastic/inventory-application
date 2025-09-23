import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL environment variable not set")
engine = create_engine(DB_URL)


def fetch_all(SQL, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(SQL), params or {})
        return result.mappings().all()


def fetch_one(SQL, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(SQL), params or {})
        return result.mappings().first()


def get_all_categories():
    SQL = """
    SELECT *
    FROM categories;
    """
    return fetch_all(SQL)


def get_category_by_id(category_id):
    SQL = """
    SELECT * FROM categories
    WHERE id = :category_id;
    """
    return fetch_one(SQL, {"category_id": category_id})


def get_all_products():
    SQL = """
    SELECT *
    FROM products;
    """
    return fetch_all(SQL)


def get_product_by_id(product_id):
    SQL = """
    SELECT * FROM products
    WHERE id = :product_id;
    """
    return fetch_one(SQL, {"product_id": product_id})


def get_products_by_category(category_id):
    SQL = """
    SELECT * FROM products
    WHERE category_id = :category_id;
    """
    return fetch_all(SQL, {"category_id": category_id})
