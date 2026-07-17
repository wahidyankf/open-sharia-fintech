"""Example 34: pytest verification for State Machine -- OO (State Pattern)."""

from example import Locked, TurnstileState, Unlocked


def test_state_pattern_trace_matches_the_imperative_version() -> None:
    events = ["coin", "push", "push", "coin", "coin", "push"]  # => same sequence as example 33
    current: TurnstileState = Locked()  # => start locked
    history = [current.name]
    for event in events:
        current = current.on_coin() if event == "coin" else current.on_push()
        history.append(current.name)
    assert history == ["locked", "unlocked", "locked", "locked", "unlocked", "unlocked", "locked"]


def test_each_transition_returns_a_distinct_state_object() -> None:
    locked = Locked()  # => construct once
    unlocked = locked.on_coin()  # => transition via a coin
    assert isinstance(unlocked, Unlocked)  # => coin from Locked always yields an Unlocked object
    assert unlocked.on_push().name == "locked"  # => push from Unlocked always yields back to locked


# => Run: pytest -- Output: 2 passed
