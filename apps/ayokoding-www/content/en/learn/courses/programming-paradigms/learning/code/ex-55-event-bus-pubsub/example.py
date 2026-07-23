"""Example 55: Event Bus Pub/Sub."""

from collections.abc import Callable  # => types every subscriber handler stored below
from dataclasses import dataclass, field  # => @dataclass generates __init__; field() gives a fresh dict
from typing import TypeVar  # => used to declare the generic payload type below

T = TypeVar("T")  # => generic payload type, so the bus is reusable for any event shape


@dataclass  # => auto-generates EventBus's __init__ from the field below
class EventBus:  # => a TYPED publish/subscribe bus: multiple subscribers per topic
    _subscribers: dict[str, list[Callable[[object], None]]] = field(default_factory=dict[str, list[Callable[[object], None]]])  # => topic -> handlers, one fresh dict per instance

    def subscribe(self, topic: str, handler: Callable[[object], None]) -> None:  # => register a subscriber
        self._subscribers.setdefault(topic, []).append(handler)  # => topics may have MANY subscribers

    def publish(self, topic: str, payload: object) -> None:  # => notify every subscriber to this topic
        for handler in self._subscribers.get(topic, []):  # => every registered handler gets a turn
            handler(payload)  # => called with the exact payload passed to publish()


bus = EventBus()  # => construct a fresh bus
seen_by_a: list[object] = []  # => subscriber A's own recorder
seen_by_b: list[object] = []  # => subscriber B's own, independent recorder

bus.subscribe("order.created", lambda payload: seen_by_a.append(payload))  # => subscriber A
bus.subscribe("order.created", lambda payload: seen_by_b.append(payload))  # => subscriber B, same topic

bus.publish("order.created", {"id": 1})  # => BOTH subscribers must be notified once each
print(seen_by_a)  # => A saw the payload
# => Output: [{'id': 1}]
print(seen_by_b)  # => B saw the SAME payload, independently
# => Output: [{'id': 1}]
