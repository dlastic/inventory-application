import os

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine


def get_engine() -> Engine:
    load_dotenv()
    db_url = os.getenv("DB_URL")
    if db_url is None:
        raise ValueError("DB_URL environment variable not set")
    return create_engine(db_url)
