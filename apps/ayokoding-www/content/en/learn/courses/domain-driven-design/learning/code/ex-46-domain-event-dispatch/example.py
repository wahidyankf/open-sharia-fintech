"""Example 46: a dispatcher sends facts to subscribed handlers."""

seen: list[str] = []  # => handler side effects are observable in a local test double


def handle(event: str) -> None:
    seen.append(event)  # => subscriber reacts without changing the producer


def publish(event: str, handlers: list[object]) -> None:
    for handler in handlers:
        handler(event)  # type: ignore[operator]  # => dispatch each subscriber


publish("OrderPlaced", [handle])
assert seen == ["OrderPlaced"]
