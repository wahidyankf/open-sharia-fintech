"""Example 86: pytest verification for the java.util.concurrent.Flow-Style Contract."""

import pytest
from example import ContractViolation, FlowPublisher, RecordingSubscriber


def test_on_subscribe_always_fires_first_and_exactly_once() -> None:
    publisher = FlowPublisher([1, 2, 3])
    subscriber = RecordingSubscriber()
    publisher.subscribe(subscriber)
    assert subscriber.log == ["subscribe"]  # => nothing else can legally happen before this


def test_on_next_only_happens_in_response_to_outstanding_demand() -> None:
    publisher = FlowPublisher([1, 2, 3, 4, 5])
    subscriber = RecordingSubscriber()
    subscription = publisher.subscribe(subscriber)
    subscription.request(2)  # => ask for exactly 2
    assert subscriber.log == ["subscribe", "next:1", "next:2"]  # => not 3, not 5 -- exactly the requested amount
    assert subscriber.terminated is False  # => 3 items remain -- not yet complete


def test_completion_is_the_only_terminal_signal_on_the_happy_path() -> None:
    publisher = FlowPublisher([1, 2])
    subscriber = RecordingSubscriber()
    subscription = publisher.subscribe(subscriber)
    subscription.request(10)  # => over-request -- production simply stops when the backlog is exhausted
    assert subscriber.log == ["subscribe", "next:1", "next:2", "complete"]
    assert subscriber.terminated is True


def test_a_producer_failure_delivers_on_error_instead_of_on_complete() -> None:
    publisher = FlowPublisher([1, 2, 3], fail_at=1)  # => fails right before emitting index 1
    subscriber = RecordingSubscriber()
    subscription = publisher.subscribe(subscriber)
    subscription.request(10)
    assert subscriber.log == ["subscribe", "next:1", "error:synthetic failure at index 1"]  # => stops right before index 1
    assert subscriber.terminated is True  # => on_error is terminal, exactly like on_complete


def test_on_next_after_a_terminal_signal_is_a_contract_violation() -> None:
    publisher = FlowPublisher([1])
    subscriber = RecordingSubscriber()
    publisher.subscribe(subscriber)
    subscriber.on_next(1)  # => manually push one value before completion, legally
    subscriber.on_complete()  # => now the stream is terminated
    with pytest.raises(ContractViolation):
        subscriber.on_next(2)  # => illegal: nothing may follow a terminal signal


# => Run: pytest -- Output: 5 passed
