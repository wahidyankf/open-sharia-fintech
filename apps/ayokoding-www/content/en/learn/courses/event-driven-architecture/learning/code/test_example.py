"""Executable checks for the Event-Driven Architecture course reference implementation."""

from dataclasses import FrozenInstanceError
import unittest

from example import (
    Event,
    EventBus,
    EventStore,
    IdempotentConsumer,
    Outbox,
    Queue,
    ReadModel,
    Saga,
    partition_for,
)


class EventDrivenArchitectureTests(unittest.TestCase):
    def test_event_is_an_immutable_fact(self) -> None:
        event = Event("1", "OrderPlaced", "o-1", {})
        with self.assertRaises(FrozenInstanceError):
            event.name = "OrderPlace"  # type: ignore[misc]

    def test_pub_sub_reaches_independent_handlers(self) -> None:
        received: list[str] = []
        bus = EventBus()
        bus.subscribe(
            "OrderPlaced", lambda item: received.append("billing:" + item.aggregate_id)
        )
        bus.subscribe(
            "OrderPlaced", lambda item: received.append("email:" + item.aggregate_id)
        )
        bus.publish(Event("1", "OrderPlaced", "o-1", {}))
        self.assertEqual(received, ["billing:o-1", "email:o-1"])

    def test_failure_isolation_preserves_other_handlers(self) -> None:
        received: list[str] = []
        bus = EventBus()
        bus.subscribe(
            "OrderPlaced", lambda _: (_ for _ in ()).throw(ValueError("broken"))
        )
        bus.subscribe("OrderPlaced", lambda item: received.append(item.aggregate_id))
        bus.publish(Event("1", "OrderPlaced", "o-1", {}))
        self.assertEqual(received, ["o-1"])
        self.assertEqual(bus.failures, ["broken"])

    def test_redelivery_is_idempotent(self) -> None:
        consumer = IdempotentConsumer()
        event = Event("same", "OrderPlaced", "o-1", {})
        self.assertTrue(consumer.handle(event))
        self.assertFalse(consumer.handle(event))
        self.assertEqual(consumer.effects, ["o-1"])

    def test_queue_dead_letters_after_bounded_retries(self) -> None:
        queue = Queue()
        queue.send(Event("poison", "OrderPlaced", "o-1", {}))
        for _ in range(3):
            event = queue.receive()
            self.assertIsNotNone(event)
            queue.nack(event)  # type: ignore[arg-type]
        self.assertEqual([item.message_id for item in queue.dead_letters], ["poison"])

    def test_replay_and_snapshot_tail_are_deterministic(self) -> None:
        store = EventStore()
        store.append(Event("1", "OrderPlaced", "o-1", {}))
        snapshot = store.replay()
        store.append(Event("2", "PaymentCaptured", "o-1", {}))
        self.assertEqual(store.replay(), {"o-1": "paid"})
        tail = EventStore(store.stream[1:]).replay(snapshot)
        self.assertEqual(tail, store.replay())

    def test_projection_can_be_rebuilt(self) -> None:
        store = EventStore(
            [
                Event("1", "OrderPlaced", "o-1", {}),
                Event("2", "PaymentCaptured", "o-1", {}),
            ]
        )
        live = ReadModel()
        for event in store.stream:
            live.project(event)
        rebuilt = ReadModel()
        for event in store.stream:
            rebuilt.project(event)
        self.assertEqual(live.orders, rebuilt.orders)

    def test_outbox_recovers_a_publish_after_the_write(self) -> None:
        outbox = Outbox()
        consumer = IdempotentConsumer()
        event = Event("1", "OrderPlaced", "o-1", {})
        outbox.commit("o-1", "placed", event)
        self.assertEqual(outbox.database["o-1"], "placed")
        outbox.relay(consumer.handle)
        outbox.relay(consumer.handle)
        self.assertEqual(consumer.effects, ["o-1"])

    def test_saga_compensates_completed_steps_in_reverse_order(self) -> None:
        saga = Saga()
        saga.step("reserve", True)
        saga.step("charge", True)
        self.assertFalse(saga.step("fulfil", False))
        self.assertEqual(saga.compensations, ["undo-charge", "undo-reserve"])

    def test_partition_key_preserves_entity_locality(self) -> None:
        self.assertEqual(partition_for("order-1", 3), partition_for("order-1", 3))


if __name__ == "__main__":
    unittest.main()
