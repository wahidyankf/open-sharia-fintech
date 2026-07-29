# pyright: strict
"""Kata 1 (after): a 429 response carries a Retry-After hint."""

from dataclasses import dataclass


@dataclass
class Response:
    status: int
    headers: dict[str, str]
    body: dict[str, str]


BUDGET = [0]  # => already exhausted


def create_order() -> Response:
    if BUDGET[0] <= 0:
        # THE FIX: include Retry-After so a client knows how long to wait before retrying.
        return Response(429, {"Retry-After": "60"}, {"error": "too many requests"})
    BUDGET[0] -= 1
    return Response(201, {}, {"status": "created"})


over_limit = create_order()
print(f"over-limit: status={over_limit.status}, headers={over_limit.headers}")
assert over_limit.headers.get("Retry-After") == "60"
