import os
import sqlite3

from dotenv import load_dotenv
from sqlalchemy import create_engine, event

load_dotenv()
db_url = os.getenv("DB_URL")
if db_url is None:
    raise ValueError("DB_URL environment variable not set")

engine = create_engine(db_url)


@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
