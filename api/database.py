import os
import psycopg2
from typing import Generator

DB_NAME     = os.getenv("DB_NAME",     "telegram_analytics")
DB_USER     = os.getenv("DB_USER",     "telegram_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345678")
DB_HOST     = os.getenv("DB_HOST",     "localhost")
DB_PORT     = os.getenv("DB_PORT",     "5432")

def get_db() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    FastAPI dependency: yield a psycopg2 connection, then close it.
    """
    conn = psycopg2.connect(
        dbname   = DB_NAME,
        user     = DB_USER,
        password = DB_PASSWORD,
        host     = DB_HOST,
        port     = DB_PORT,
    )
    try:
        yield conn
    finally:
        conn.close()
