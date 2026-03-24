"""
Safe execution layer for model-generated SQL.

Only single SELECT statements are executed. Results are returned as
list[dict] for JSON serialization. SQL errors are raised to the route
for HTTP error mapping.
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Engine


def validate_readonly_select(sql: str) -> str:
    """
    Ensure the statement is a single SELECT (or WITH … SELECT) for read-only use.

    Validation is intentionally shallow: combined with a read-only SQLite file
    for the default database, this blocks obvious multi-statement abuse. A full
    SQL parser would be stronger for untrusted natural-language backends.

    Returns:
        Normalized SQL (trailing semicolon removed).

    Raises:
        ValueError: If the query fails validation.
    """
    cleaned = sql.strip()
    if not cleaned:
        raise ValueError("Empty SQL after generation.")

    # Single statement: allow one optional trailing semicolon only.
    without_trailing = cleaned.rstrip().rstrip(";").strip()
    if ";" in without_trailing:
        raise ValueError("Multiple SQL statements are not allowed.")

    upper = without_trailing.upper()
    if not (upper.startswith("SELECT") or upper.startswith("WITH")):
        raise ValueError("Only SELECT (or WITH … SELECT) queries are allowed.")

    return without_trailing


def execute_sql(engine: Engine, query: str) -> list[dict]:
    """
    Run validated SELECT and return rows as dictionaries.

    Column names come from the cursor keys.
    """
    safe_sql = validate_readonly_select(query)
    stmt = text(safe_sql)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        keys = result.keys()
        rows = [dict(zip(keys, row)) for row in result.fetchall()]

    return rows
