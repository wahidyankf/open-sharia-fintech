"""Kata 8 (after): composition over inheritance -- EventLog HOLDS a list, sort() is simply not part of its interface."""

from __future__ import annotations

from typing import Iterator


class EventLog:  # => has-a list -- never subclasses list, so no leaked method can ever be called
    def __init__(self) -> None:
        self._events: list[str] = []

    def record(self, event: str) -> None:
        self._events.append(event)

    def __iter__(self) -> Iterator[str]:
        return iter(self._events)

    def __repr__(self) -> str:
        return repr(self._events)


log = EventLog()
log.record("login")
log.record("purchase")
log.record("logout")
print(log)  # chronological order is now structurally guaranteed -- sort() does not exist on this class
