# pyright: strict
"""Kata 1 (before): a 429 response is returned but with NO Retry-After hint."""

from dataclasses import dataclass


@dataclass
class Response:
    status: int
    headers: dict[str, str]
    body: dict[str, str]


BUDGET = [0]  # => already exhausted


def create_order() -> Response:
    # THE BUG: over-the-limit returns 429 but omits Retry-After, so a client has
    # no machine-readable hint how long to wait -- it must guess or retry-blind.
    if BUDGET[0] <= 0:
        return Response(429, {}, {"error": "too many requests"})  # BUG: no Retry-After header
    BUDGET[0] -= 1
    return Response(201, {}, {"status": "created"})


over_limit = create_order()
print(f"over-limit: status={over_limit.status}, headers={over_limit.headers}")
