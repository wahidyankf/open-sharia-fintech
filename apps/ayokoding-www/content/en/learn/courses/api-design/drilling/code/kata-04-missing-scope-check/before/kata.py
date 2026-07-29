# pyright: strict
"""Kata 4 (before): a bearer token is validated, but its SCOPE is never checked."""

VALID_TOKENS: dict[str, list[str]] = {"tok-readonly": ["articles:read"]}


def delete_article(token: str) -> int:
    # THE BUG: presence and validity of the token is checked (401 if missing/unknown),
    # but the token's OWN scopes are never inspected against what this operation needs.
    if token not in VALID_TOKENS:
        return 401
    return 204  # BUG: a read-only token can delete -- no scope gate at all


status = delete_article("tok-readonly")  # a token that can only READ articles
print(f"delete with read-only token: status={status}")  # BUG: 204, should be 403
