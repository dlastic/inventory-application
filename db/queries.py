import os

from sqlalchemy import create_engine, text

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


def execute_write(SQL, params=None):
    with engine.begin() as conn:
        conn.execute(text(SQL), params or {})


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


def add_category(name, description=None):
    SQL = """
    INSERT INTO categories (name, description)
    VALUES (:name, :description);
    """
    execute_write(SQL, {"name": name, "description": description})


def update_category(category_id, name, description=None):
    SQL = """
    UPDATE categories
    SET name = :name,
        description = :description,
        updated_at = NOW()
    WHERE id = :category_id;
    """
    execute_write(
        SQL, {"category_id": category_id, "name": name, "description": description}
    )


def delete_category(category_id):
    SQL = """
    DELETE FROM categories
    WHERE id = :category_id;
    """
    execute_write(SQL, {"category_id": category_id})


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


def add_product(name, description, price, stock, category_id):
    SQL = """
    INSERT INTO products (name, description, price, stock, category_id)
    VALUES (:name, :description, :price, :stock, :category_id)
    """
    return execute_write(
        SQL,
        {
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "category_id": category_id,
        },
    )


def edit_product(product_id, name, description, price, stock, category_id):
    SQL = """
    UPDATE products
    SET name = :name,
        description = :description,
        price = :price,
        stock = :stock,
        category_id = :category_id,
        updated_at = NOW()
    WHERE id = :product_id;
    """
    execute_write(
        SQL,
        {
            "product_id": product_id,
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "category_id": category_id,
        },
    )


def delete_product(product_id):
    SQL = """
    DELETE FROM products
    WHERE id = :product_id;
    """
    execute_write(SQL, {"product_id": product_id})
