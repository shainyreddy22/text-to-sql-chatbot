"""
FastAPI entrypoint for the Text-to-SQL chatbot backend.
"""

import logging

from fastapi import FastAPI

from app.routes import router

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Text-to-SQL Bot",
    description="Natural language to SQL over SQLite (Gemini + LangChain). "
    "Responses include result data only, not generated SQL.",
    version="1.0.0",
)

app.include_router(router)
