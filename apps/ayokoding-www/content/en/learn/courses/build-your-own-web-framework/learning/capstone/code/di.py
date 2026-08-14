"""Capstone request-scoped dependency."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RankingService:
    # => The value is immutable so the handler cannot mutate shared global state.
    items: tuple[str, ...]


def per_request_service() -> RankingService:
    # => A new instance is created each time the framework resolves this dependency.
    return RankingService(("framework", "router", "middleware"))
