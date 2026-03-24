"""
LLM integration: natural language → SQL using LangChain + Google Gemini.

The returned SQL string is for internal use only; the API never exposes it.
"""

from __future__ import annotations

import os
import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


def _strip_sql_fences(raw: str) -> str:
    """Remove optional Markdown ```sql ... ``` wrapping from model output."""
    text = raw.strip()
    fence = re.match(r"^```(?:sql)?\s*\n?(.*?)\n?```$", text, re.DOTALL | re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    return text


def generate_sql(user_query: str, schema: str) -> str:
    """
    Ask Gemini to produce a single SQLite SELECT statement for the question.

    Raises:
        ValueError: If GOOGLE_API_KEY is missing or the model returns empty text.
    """
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN", "").strip()
    if not api_key:
        raise ValueError(
            "HUGGINGFACEHUB_API_TOKEN is not set. Add it to your .env file."
        )

    model_name = os.getenv("HUGGINGFACE_REPO_ID", "Qwen/Qwen2.5-Coder-32B-Instruct").strip()

    system_prompt = (
        "You are a SQL expert. Convert the user question into a correct SQL query.\n"
        f"Database schema:\n{schema}\n\n"
        "Rules:\n\n"
        "- Only return SQL\n"
        "- No explanation\n"
        "- Use LIMIT when needed\n"
        "- Use ORDER BY for 'recent' queries"
    )

    base_llm = HuggingFaceEndpoint(
        repo_id=model_name,
        huggingfacehub_api_token=api_key,
        task="text-generation",
        max_new_tokens=512,
        temperature=0.01,
        repetition_penalty=1.03,
    )
    llm = ChatHuggingFace(llm=base_llm)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query.strip()),
    ]

    response = llm.invoke(messages)
    content = getattr(response, "content", None) or ""
    if isinstance(content, list):
        # Some message formats return structured parts.
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )

    sql = _strip_sql_fences(str(content).strip())
    if not sql:
        raise ValueError("The model returned an empty SQL string.")

    return sql
