# pyright: strict
"""Kata 5 (after): the resolver returns exactly (and only) the requested fields."""

from typing import Any

ARTICLE: dict[str, object] = {"id": 1, "title": "Hello, GraphQL", "body": "A very long article body..."}


def resolve_article(requested_fields: list[str]) -> dict[str, Any]:
    # THE FIX: build the response from ONLY the fields the caller's own query named.
    selected = {field: ARTICLE[field] for field in requested_fields if field in ARTICLE}
    return {"data": {"article": selected}}


narrow_query = resolve_article(["title"])
print(f"caller asked for ['title'], got: {narrow_query}")
