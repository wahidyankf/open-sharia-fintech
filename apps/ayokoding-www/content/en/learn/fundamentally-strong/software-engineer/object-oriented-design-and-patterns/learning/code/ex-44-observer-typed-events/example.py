"""Example 44: A Typed Event Bus with Unsubscribe."""

from collections.abc import Callable  # => imports Callable from collections.abc

Handler = Callable[[str], None]  # => a type alias: any function taking str, returning None


class EventBus:  # => the SUBJECT -- notifies subscribers without knowing their concrete type
    def __init__(self) -> None:  # => the constructor
        self._handlers: dict[str, list[Handler]] = {}  # => topic name -> list of subscribers

    def subscribe(self, topic: str, handler: Handler) -> None:  # => defines subscribe()
        self._handlers.setdefault(topic, []).append(handler)  # => adds this handler to the topic's list

    def unsubscribe(self, topic: str, handler: Handler) -> None:  # => defines unsubscribe()
        self._handlers.get(topic, []).remove(handler)  # => removes ONLY this handler, leaves others intact

    def publish(self, topic: str, message: str) -> None:  # => defines the publish() method
        for handler in self._handlers.get(topic, []):  # => notifies EVERY currently-subscribed handler
            handler(message)  # => the bus never knows or cares what each handler DOES


received: list[str] = []  # => a plain list used to OBSERVE which handlers actually fired


def log_handler(message: str) -> None:  # => one concrete subscriber
    received.append(f"log: {message}")  # => records that this handler ran


def alert_handler(message: str) -> None:  # => a DIFFERENT concrete subscriber
    received.append(f"alert: {message}")  # => records that this handler ran


bus: EventBus = EventBus()  # => constructs bus
bus.subscribe("order.created", log_handler)  # => subscribes log_handler to this topic
bus.subscribe("order.created", alert_handler)  # => subscribes alert_handler to the SAME topic

bus.publish("order.created", "order-1")  # => notifies BOTH currently-subscribed handlers
print(received)  # => both handlers ran, in subscription order
# => Output: ['log: order-1', 'alert: order-1']

bus.unsubscribe("order.created", alert_handler)  # => alert_handler is no longer subscribed
received.clear()  # => resets the observation list for the next publish
bus.publish("order.created", "order-2")  # => notifies only whichever handlers remain
print(received)  # => alert_handler did NOT run -- it was unsubscribed above
# => Output: ['log: order-2']
# => `unsubscribe` removes exactly one handler from one topic; every other subscription is unaffected
