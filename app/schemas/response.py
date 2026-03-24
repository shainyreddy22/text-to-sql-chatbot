"""Pydantic response models for the API."""

from typing import Any

from pydantic import BaseModel, Field


class QueryResponse(BaseModel):
    """Query result rows only (SQL is never exposed)."""

    data: list[dict[str, Any]] = Field(default_factory=list)
