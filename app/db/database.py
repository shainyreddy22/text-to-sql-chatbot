"""
Database configuration and schema introspection for SQLite.

Uses SQLAlchemy. The default database path points to the Chinook sample
found under the user's Downloads folder; override with DATABASE_URL in .env.
"""

from __future__ import annotations

import os
import sqlite3
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# Default: Chinook SQLite discovered in Downloads (user request).
_DEFAULT_SQLITE = Path.home() / "Downloads" / "Chinook_Sqlite.sqlite"


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for optional ORM models."""

    pass


def _default_sqlite_readonly_connection() -> sqlite3.Connection:
    """Open the default Chinook file in read-only mode (Windows-safe)."""
    path = _DEFAULT_SQLITE.resolve()
    if not path.is_file():
        raise FileNotFoundError(
            f"Default SQLite database not found at {path}. "
            "Set DATABASE_URL in .env to your SQLite file path."
        )
    # sqlite3 URI form works reliably across platforms when uri=True.
    return sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True, check_same_thread=False)


@lru_cache
def get_engine() -> Engine:
    """
    Return a cached SQLAlchemy Engine.

    If ``DATABASE_URL`` is set, it is used as a normal SQLAlchemy URL.
    Otherwise the default Downloads Chinook database is opened read-only
    via a custom connection factory.
    """
    explicit = os.getenv("DATABASE_URL", "").strip()
    if explicit:
        return create_engine(explicit, connect_args={"check_same_thread": False})

    if not _DEFAULT_SQLITE.is_file():
        raise FileNotFoundError(
            f"Default SQLite database not found at {_DEFAULT_SQLITE.resolve()}. "
            "Set DATABASE_URL in .env to your SQLite file path."
        )

    return create_engine(
        "sqlite://",
        creator=_default_sqlite_readonly_connection,
    )


def get_session_factory():
    """Session factory for routes that need explicit sessions."""
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


@lru_cache(maxsize=1)
def get_schema_for_prompt() -> str:
    """
    Load CREATE TABLE statements from sqlite_master for LLM context.

    Excludes internal SQLite tables. This keeps the bot accurate for whatever
    database file is configured (e.g. Chinook in Downloads).
    """
    engine = get_engine()
    stmt = text(
        """
        SELECT sql FROM sqlite_master
        WHERE type = 'table'
          AND sql IS NOT NULL
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()
    parts = [r[0] for r in rows if r[0]]
    return "\n\n".join(parts) if parts else "(no tables found)"
