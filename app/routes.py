"""
HTTP routes: POST /query runs the Text-to-SQL pipeline.

Response body contains only ``data`` (result rows). SQL is never returned.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.db.database import get_engine, get_schema_for_prompt
from app.schemas.request import QueryRequest
from app.schemas.response import QueryResponse
from app.services.llm_service import generate_sql
from app.services.sql_service import execute_sql

logger = logging.getLogger(__name__)

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
def run_query(body: QueryRequest) -> QueryResponse:
    """
    Convert natural language to SQL, execute, return rows only.
    """
    try:
        schema = get_schema_for_prompt()
        sql = generate_sql(body.question, schema)
        logger.debug("Generated SQL (not sent to client): %s", sql)
        engine = get_engine()
        rows = execute_sql(engine, sql)
        return QueryResponse(data=rows)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    except Exception as e:
        logger.exception("Query pipeline failed")
        raise HTTPException(
            status_code=502,
            detail="The query could not be completed. Try rephrasing your question.",
        ) from e
