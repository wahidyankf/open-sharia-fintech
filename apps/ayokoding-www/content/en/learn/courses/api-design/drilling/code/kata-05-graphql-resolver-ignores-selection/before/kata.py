# pyright: strict
"""Kata 5 (before): the resolver returns the FULL record, ignoring the caller's field selection."""

from typing import Any

ARTICLE: dict[str, object] = {"id": 1, "title": "Hello, GraphQL", "body": "A very long article body..."}


def resolve_article(requested_fields: list[str]) -> dict[str, Any]:
    # THE BUG: `requested_fields` is accepted as a parameter but never used to
    # narrow the response -- the caller always gets EVERY field, defeating the
    # entire over-fetch-avoidance point of a GraphQL selection set.
    return {"data": {"article": ARTICLE}}


narrow_query = resolve_article(["title"])  # the caller asked for ONLY title
print(f"caller asked for ['title'], got: {narrow_query}")  # BUG: id and body leak through too
