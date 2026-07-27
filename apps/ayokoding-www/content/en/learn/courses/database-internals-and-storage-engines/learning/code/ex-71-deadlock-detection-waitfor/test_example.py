"""Example 71: pytest verification for Deadlock Detection via a Wait-For Graph."""

from example import choose_victim, has_cycle


def test_a_circular_wait_is_detected_as_a_cycle() -> None:
    wait_for = {10: 20, 20: 10}
    cycle = has_cycle(wait_for)
    assert cycle is not None


def test_a_victim_is_chosen_from_within_the_detected_cycle() -> None:
    wait_for = {10: 20, 20: 10}
    cycle = has_cycle(wait_for)
    assert cycle is not None
    victim = choose_victim(cycle)
    assert victim in cycle


# => Run: pytest -- Output: 2 passed
