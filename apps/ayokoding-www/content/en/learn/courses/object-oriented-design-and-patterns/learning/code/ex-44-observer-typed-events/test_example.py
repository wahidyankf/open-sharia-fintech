"""Example 44: pytest verification for the Typed Event Bus with Unsubscribe."""

from example import EventBus


def test_every_subscribed_handler_receives_a_published_event() -> None:
    received: list[str] = []
    bus: EventBus = EventBus()
    bus.subscribe("topic", lambda msg: received.append(f"a:{msg}"))
    bus.subscribe("topic", lambda msg: received.append(f"b:{msg}"))
    bus.publish("topic", "hello")
    assert received == ["a:hello", "b:hello"]  # => both handlers fired


def test_unsubscribed_handler_is_not_called() -> None:
    received: list[str] = []

    def handler(msg: str) -> None:
        received.append(msg)

    bus: EventBus = EventBus()
    bus.subscribe("topic", handler)
    bus.unsubscribe("topic", handler)  # => removed BEFORE any publish() call
    bus.publish("topic", "hello")
    assert received == []  # => the unsubscribed handler never ran


# => Run: pytest -- Output: 2 passed
