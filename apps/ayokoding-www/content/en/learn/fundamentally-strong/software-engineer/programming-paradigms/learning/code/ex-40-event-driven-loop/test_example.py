"""Example 40: pytest verification for Event-Driven Loop."""

from collections import deque
from collections.abc import Callable

from example import Event


def test_events_processed_in_fifo_order() -> None:
    seen: list[str] = []  # => local recorder, isolated from the module-level demo
    handlers: dict[str, Callable[[Event], None]] = {
        "login": lambda e: seen.append(f"login:{e.payload}"),
        "logout": lambda e: seen.append(f"logout:{e.payload}"),
    }
    queue = deque([Event("login", "x"), Event("logout", "y"), Event("login", "z")])
    while queue:
        event = queue.popleft()
        handlers[event.kind](event)
    assert seen == ["login:x", "logout:y", "login:z"]  # => exactly the enqueue order, unchanged


def test_named_handlers_produce_the_documented_module_level_trace() -> None:
    from example import processed  # => the module-level demo already ran when example.py was imported

    assert processed == ["login:alice", "login:bob", "logout:alice"]  # => matches example.py's own Output


# => Run: pytest -- Output: 2 passed
