"""Runnable event-driven architecture reference used by the course examples.

The implementation is deliberately in-process: its job is to expose invariants, not to imitate a
particular vendor client. Every persistent-looking collection is copied where ownership changes so
the examples cannot accidentally prove correctness by sharing mutable state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Event:
    """An immutable fact, named in the past tense, with a schema version and stable message id."""

    message_id: str
    name: str
    aggregate_id: str
    payload: dict[str, str]
    version: int = 1


Handler = Callable[[Event], None]


@dataclass
class EventBus:
    """Synchronous pub/sub with failure isolation for teaching deterministic delivery."""

    handlers: dict[str, list[Handler]] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)

    def subscribe(self, event_name: str, handler: Handler) -> Callable[[], None]:
        self.handlers.setdefault(event_name, []).append(handler)

        def unsubscribe() -> None:
            self.handlers[event_name].remove(handler)

        return unsubscribe

    def publish(self, event: Event) -> None:
        for handler in list(self.handlers.get(event.name, [])):
            try:
                handler(event)
            except ValueError as error:
                self.failures.append(str(error))


@dataclass
class Queue:
    """A tiny at-least-once queue: nack requeues and ack removes one delivery."""

    pending: list[Event] = field(default_factory=list)
    dead_letters: list[Event] = field(default_factory=list)
    attempts: dict[str, int] = field(default_factory=dict)

    def send(self, event: Event) -> None:
        self.pending.append(event)

    def receive(self) -> Event | None:
        if not self.pending:
            return None
        event = self.pending.pop(0)
        self.attempts[event.message_id] = self.attempts.get(event.message_id, 0) + 1
        return event

    def nack(self, event: Event, limit: int = 3) -> None:
        if self.attempts[event.message_id] >= limit:
            self.dead_letters.append(event)
        else:
            self.pending.append(event)


@dataclass
class EventStore:
    """Append-only stream with deterministic fold and snapshot-plus-tail replay."""

    stream: list[Event] = field(default_factory=list)

    def append(self, event: Event) -> None:
        self.stream.append(event)

    def replay(self, initial: dict[str, str] | None = None) -> dict[str, str]:
        state = dict(initial or {})
        for event in self.stream:
            if event.name == "OrderPlaced":
                state[event.aggregate_id] = "placed"
            elif event.name == "PaymentCaptured":
                state[event.aggregate_id] = "paid"
            elif event.name == "OrderCancelled":
                state[event.aggregate_id] = "cancelled"
        return state


@dataclass
class ReadModel:
    """A denormalized projection that intentionally updates after the write stream."""

    orders: dict[str, str] = field(default_factory=dict)

    def project(self, event: Event) -> None:
        if event.name == "OrderPlaced":
            self.orders[event.aggregate_id] = "placed"
        if event.name == "PaymentCaptured":
            self.orders[event.aggregate_id] = "paid"
        if event.name == "OrderCancelled":
            self.orders[event.aggregate_id] = "cancelled"


@dataclass
class Outbox:
    """Models the transaction boundary: state and unpublished event enter together."""

    database: dict[str, str] = field(default_factory=dict)
    rows: list[tuple[Event, bool]] = field(default_factory=list)

    def commit(self, order_id: str, state: str, event: Event) -> None:
        self.database[order_id] = state
        self.rows.append((event, False))

    def relay(self, publish: Callable[[Event], object]) -> None:
        for index, (event, published) in enumerate(self.rows):
            if not published:
                publish(event)
                self.rows[index] = (event, True)


@dataclass
class IdempotentConsumer:
    """Records message ids before applying their externally visible effect."""

    processed: set[str] = field(default_factory=set)
    effects: list[str] = field(default_factory=list)

    def handle(self, event: Event) -> bool:
        if event.message_id in self.processed:
            return False
        self.processed.add(event.message_id)
        self.effects.append(event.aggregate_id)
        return True


@dataclass
class Saga:
    """Records completed local steps and compensates exactly those steps in reverse order."""

    completed: list[str] = field(default_factory=list)
    compensations: list[str] = field(default_factory=list)

    def step(self, name: str, succeeds: bool) -> bool:
        if succeeds:
            self.completed.append(name)
            return True
        for completed in reversed(self.completed):
            self.compensations.append(f"undo-{completed}")
        return False


def partition_for(key: str, partitions: int) -> int:
    """A stable, process-independent partition choice for deterministic examples."""

    return sum(ord(character) for character in key) % partitions


def demo() -> None:
    event = Event("m-1", "OrderPlaced", "order-1", {"total": "42"})
    store = EventStore()
    store.append(event)
    store.append(Event("m-2", "PaymentCaptured", "order-1", {}))
    projection = ReadModel()
    for item in store.stream:
        projection.project(item)
    outbox = Outbox()
    outbox.commit("order-2", "placed", Event("m-3", "OrderPlaced", "order-2", {}))
    consumer = IdempotentConsumer()
    outbox.relay(consumer.handle)
    outbox.relay(consumer.handle)
    saga = Saga()
    saga.step("reserve-inventory", True)
    saga.step("capture-payment", False)
    queue = Queue()
    poison = Event("m-4", "OrderPlaced", "order-3", {})
    queue.send(poison)
    for _ in range(3):
        received = queue.receive()
        assert received is not None
        queue.nack(received)
    print(store.replay()["order-1"])
    print(projection.orders["order-1"])
    print(consumer.effects)
    print(saga.compensations)
    print([item.message_id for item in queue.dead_letters])


if __name__ == "__main__":
    demo()
