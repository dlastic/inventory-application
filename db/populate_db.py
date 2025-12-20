from sqlalchemy import text

from db.connection import get_engine

SQL = """
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER DEFAULT 1 REFERENCES categories(id) ON DELETE SET DEFAULT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO categories (name, description) VALUES
  ('Uncategorized', 'Default category for uncategorized products'),
  ('Computers & Laptops', 'Desktops, laptops, and accessories'),
  ('Phones & Tablets', 'Smartphones, tablets, and related devices'),
  ('TVs & Audio', 'Televisions, sound systems, and audio equipment'),
  ('Gaming', 'Consoles, games, and gaming accessories'),
  ('Home Appliances', 'Electronics and appliances for the home');

INSERT INTO products (name, description, price, stock, category_id) VALUES
  ('MacBook Pro 14"', 'Apple laptop with M2 Pro chip', 1999.99, 10, 2),
  ('Dell XPS 13', 'Compact Windows ultrabook', 1399.99, 15, 2),
  ('Lenovo ThinkPad X1', 'Business laptop with great keyboard', 1299.99, 20, 2),
  ('LG Gram 16', 'Ultra-lightweight laptop', 1499.99, 12, 2),
  ('Sony Vaio Z', 'High-performance ultrabook', 1799.99, 8, 2),

  ('iPhone 15', 'Latest Apple smartphone', 1199.99, 25, 3),
  ('Samsung Galaxy S24', 'Flagship Android phone', 1099.99, 30, 3),
  ('Sony Xperia 5', 'Compact Android phone', 899.99, 18, 3),
  ('iPad Pro 12.9"', 'Apple high-end tablet', 1399.99, 14, 3),
  ('Samsung Galaxy Tab S9', 'Premium Android tablet', 999.99, 20, 3),

  ('LG OLED55', '55-inch OLED TV', 1499.99, 12, 4),
  ('Sony Bravia XR', '65-inch 4K HDR TV', 1999.99, 10, 4),
  ('Samsung QLED Q90', 'High-end QLED TV', 1799.99, 9, 4),
  ('Apple HomePod', 'Smart speaker with high-fidelity sound', 299.99, 25, 4),
  ('Sony WH-1000XM5', 'Noise-cancelling headphones', 399.99, 40, 4),

  ('PlayStation 5', 'Sony next-gen console', 499.99, 20, 5),
  ('Xbox Series X', 'Microsoft flagship console', 499.99, 18, 5),
  ('Nintendo Switch OLED', 'Portable hybrid console', 349.99, 25, 5),
  ('Alienware Gaming Laptop', 'High-performance gaming laptop', 2299.99, 7, 5),
  ('LG Ultragear Monitor', 'High refresh rate gaming monitor', 599.99, 15, 6),

  ('Roomba i7', 'Robot vacuum cleaner', 599.99, 22, 6),
  ('LG Air Purifier', 'Removes dust and allergens', 399.99, 17, 6),
  ('Samsung Family Hub Fridge', 'Smart refrigerator with touchscreen', 2999.99, 5, 6),
  ('Sony Bluetooth Speaker', 'Portable speaker with deep bass', 149.99, 30, 6),
  ('Apple AirPods Pro 2', 'Noise-cancelling wireless earbuds', 249.99, 35, 6);
"""


def main() -> None:
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(SQL))
    print("Database populated with initial data.")


if __name__ == "__main__":
    main()
