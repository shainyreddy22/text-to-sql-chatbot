"""
ORM models (optional extension layer).

The Text-to-SQL flow uses dynamic schema introspection in ``database.py`` so it
works with the SQLite file in Downloads (e.g. Chinook) without hand-written
models. Subclass ``Base`` here if you add migrations or ORM-backed tables.
"""

from app.db.database import Base

__all__ = ["Base"]
