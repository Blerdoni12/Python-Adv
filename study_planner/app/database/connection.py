import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.utils.config import Settings

settings = Settings()


def get_db_connection() -> sqlite3.Connection:
    db_dir = Path(settings.db_path).parent
    db_dir.mkdir(exist_ok=True)
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def db_session() -> Iterator[sqlite3.Connection]:
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
