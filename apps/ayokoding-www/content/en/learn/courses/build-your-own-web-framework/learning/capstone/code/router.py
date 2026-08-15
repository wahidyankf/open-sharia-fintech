"""Capstone route lookup."""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    # => A response stays a value until the WSGI edge serializes it.
    status: int
    body: bytes


Handler = Callable[[], Response]


def resolve(path: str) -> Handler:
    # => The table maps a path to a handler; the fallback is an explicit 404.
    routes: dict[str, Handler] = {"/health": lambda: Response(200, b'{"status":"ok"}')}
    return routes.get(path, lambda: Response(404, b'{"detail":"not found"}'))
