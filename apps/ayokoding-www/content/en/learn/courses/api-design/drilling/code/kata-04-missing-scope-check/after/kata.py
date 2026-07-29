# pyright: strict
"""Kata 4 (after): the required scope is checked before performing the write."""

VALID_TOKENS: dict[str, list[str]] = {"tok-readonly": ["articles:read"]}
REQUIRED_SCOPE = "articles:delete"


def delete_article(token: str) -> int:
    if token not in VALID_TOKENS:
        return 401
    # THE FIX: the token's OWN scopes must include what this operation requires.
    if REQUIRED_SCOPE not in VALID_TOKENS[token]:
        return 403
    return 204


status = delete_article("tok-readonly")
print(f"delete with read-only token: status={status}")
