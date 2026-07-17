"""Example 35: pytest verification for State Machine -- Functional."""

from example import transition


def test_pure_transition_matches_the_other_two_versions() -> None:
    from functools import reduce

    events = ["coin", "push", "push", "coin", "coin", "push"]  # => same sequence as examples 33-34
    history = reduce(lambda states, event: states + [transition(states[-1], event)], events, ["locked"])
    assert history == ["locked", "unlocked", "locked", "locked", "unlocked", "unlocked", "locked"]


def test_transition_never_mutates_its_string_arguments() -> None:
    before_state, before_event = "locked", "coin"  # => strings are immutable in Python regardless,
    result = transition(before_state, before_event)  # => but this documents the pure-function contract
    assert before_state == "locked" and before_event == "coin"  # => arguments are provably unchanged
    assert result == "unlocked"  # => and the correct new state was returned as a NEW value


# => Run: pytest -- Output: 2 passed
