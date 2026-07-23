"""Tests for the reactive Sequential Transaction Processor."""

from paradigms.reactive import ReactiveAccount, process_transactions_reactive


def test_matches_the_shared_expected_result() -> None:
    balance, rejected = process_transactions_reactive([50, -200, 30, -1000, 20], starting_balance=100)
    assert (balance, rejected) == (200, [1, 3])


def test_rejection_subscriber_is_pushed_automatically_not_polled() -> None:
    account = ReactiveAccount(starting_balance=0)
    seen: list[int] = []  # => local recorder, filled only via the push callback
    account.on_reject(lambda index: seen.append(index))
    account.apply(0, -5)  # => would go negative -- must push a rejection notification immediately
    assert seen == [0]  # => the subscriber saw it without ever polling the account


def test_multiple_subscribers_are_all_notified_of_the_same_rejection() -> None:
    account = ReactiveAccount(starting_balance=0)
    seen_a: list[int] = []
    seen_b: list[int] = []
    account.on_reject(lambda index: seen_a.append(index))
    account.on_reject(lambda index: seen_b.append(index))
    account.apply(3, -1)  # => one rejection event
    assert seen_a == [3]
    assert seen_b == [3]  # => both subscribers received the same push, independently
