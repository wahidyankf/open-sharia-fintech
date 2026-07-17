"""Example 64: pytest verification for Event Sourcing Fold."""

from functools import reduce

from example import AccountState, Event, apply_event


def test_replay_reproduces_the_live_state() -> None:
    log = [Event("opened"), Event("deposited", 100), Event("deposited", 50), Event("withdrawn", 30)]
    live = reduce(apply_event, log, AccountState())  # => same log as the module-level demo
    replayed = reduce(apply_event, log, AccountState())  # => a completely independent second fold
    assert live == replayed == AccountState(balance=120, is_open=True)


def test_events_are_never_mutated_by_folding_over_them() -> None:
    log = [Event("opened"), Event("deposited", 10)]  # => a small log
    before = list(log)  # => snapshot before folding
    reduce(apply_event, log, AccountState())  # => fold once, discard the result
    assert log == before  # => the event list itself is untouched -- events are read-only facts


# => Run: pytest -- Output: 2 passed
