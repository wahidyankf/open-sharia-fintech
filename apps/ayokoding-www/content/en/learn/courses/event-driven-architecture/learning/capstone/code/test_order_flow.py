"""Tests for the local-broker Event-Driven Architecture capstone."""

import unittest

from order_flow import Fact, OrderFlow


class OrderFlowTests(unittest.TestCase):
    def test_replay_rebuilds_the_same_read_state(self) -> None:
        flow = OrderFlow()
        event = flow.place("o-1")
        flow.relay()
        flow.consume(event)
        self.assertEqual(flow.replay(), flow.read_model)

    def test_outbox_recovers_and_idempotency_handles_redelivery(self) -> None:
        flow = OrderFlow()
        event = flow.place("o-1")
        flow.relay()
        self.assertTrue(flow.consume(event))
        self.assertFalse(flow.consume(event))
        self.assertEqual(flow.read_model, {"o-1": "placed"})

    def test_failed_saga_compensates_completed_inventory_work(self) -> None:
        flow = OrderFlow()
        self.assertFalse(flow.saga(payment_succeeds=False))
        self.assertEqual(flow.compensations, ["release-inventory"])

    def test_poison_event_reaches_the_dlq(self) -> None:
        flow = OrderFlow()
        poison = Fact("poison:o-2", "OrderPlaced", "o-2")
        self.assertFalse(flow.consume(poison, poison=True))
        self.assertEqual(flow.dead_letters, [poison])


if __name__ == "__main__":
    unittest.main()
