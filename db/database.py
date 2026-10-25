"""Соединения SQLite и именованные запросы из единого SQL-файла."""
import os
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tenant_requests.sqlite"
QUERY_TEXT = (BASE_DIR / "sql" / "queries.sql").read_text(encoding="utf-8")
QUERIES = {
    match.group(1): match.group(2).strip()
    for match in re.finditer(
        r"-- name: (\w+)\n(.*?)(?=-- name: |\Z)", QUERY_TEXT, re.S
    )
}


@contextmanager
def connect(path=None):
    """Закрыть соединение и при исключении откатить изменения."""
    conn = sqlite3.connect(path or os.environ.get("TENANT_REQUESTS_DB") or DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch(name, params=(), one=False):
    """Выполнить SELECT с параметрами; соединение закрывается после чтения."""
    with connect() as conn:
        cursor = conn.execute(QUERIES[name], params)
        return cursor.fetchone() if one else cursor.fetchall()
