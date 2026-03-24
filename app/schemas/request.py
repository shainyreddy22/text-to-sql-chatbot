"""Pydantic request models for the API."""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Natural language question from the client."""

    question: str = Field(
        ...,
        min_length=1,
        description="User question to translate into SQL and run.",
    )
