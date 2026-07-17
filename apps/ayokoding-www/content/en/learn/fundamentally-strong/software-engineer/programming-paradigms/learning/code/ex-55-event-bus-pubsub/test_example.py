"""Example 55: pytest verification for Event Bus Pub/Sub."""

from example import EventBus


def test_all_subscribers_notified_exactly_once_each() -> None:
    bus = EventBus()  # => fresh bus, isolated from the module-level demo
    counts = {"a": 0, "b": 0, "c": 0}  # => local recorder for three subscribers
    bus.subscribe("topic", lambda payload: counts.__setitem__("a", counts["a"] + 1))
    bus.subscribe("topic", lambda payload: counts.__setitem__("b", counts["b"] + 1))
    bus.subscribe("topic", lambda payload: counts.__setitem__("c", counts["c"] + 1))
    bus.publish("topic", {"x": 1})  # => publish exactly once
    assert counts == {"a": 1, "b": 1, "c": 1}  # => every subscriber fired exactly once


def test_subscribers_on_a_different_topic_are_not_notified() -> None:
    bus = EventBus()  # => fresh bus
    seen: list[object] = []  # => local recorder
    bus.subscribe("topic.a", lambda payload: seen.append(payload))  # => subscribed to topic.a only
    bus.publish("topic.b", {"unrelated": True})  # => publish to a DIFFERENT topic
    assert seen == []  # => the topic.a subscriber was never called


# => Run: pytest -- Output: 2 passed
