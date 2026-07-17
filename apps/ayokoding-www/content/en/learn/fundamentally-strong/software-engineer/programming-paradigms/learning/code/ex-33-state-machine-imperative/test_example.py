"""Example 33: pytest verification for State Machine -- Imperative."""

import example


def test_locked_to_unlocked_to_locked_sequence() -> None:
    # => the module-level demo already replayed coin,push,push,coin,coin,push -- verify its trace
    assert example.history == ["locked", "unlocked", "locked", "locked", "unlocked", "unlocked", "locked"]


def test_pushing_a_locked_turnstile_does_not_unlock_it() -> None:
    example.state = "locked"  # => reset the shared global explicitly for this test's own run
    example.handle("push")  # => push while locked
    assert example.state == "locked"  # => must remain locked -- pushing alone never unlocks


# => Run: pytest -- Output: 2 passed
