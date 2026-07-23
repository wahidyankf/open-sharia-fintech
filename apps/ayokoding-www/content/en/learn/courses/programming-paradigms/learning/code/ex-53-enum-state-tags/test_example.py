"""Example 53: pytest verification for Enum State Tags."""

from example import LightState, next_state


def test_full_transition_cycle_returns_to_the_start() -> None:
    state = LightState.RED  # => start fresh, isolated from the module-level demo
    for _ in range(3):  # => a full red -> green -> yellow -> red cycle
        state = next_state(state)
    assert state == LightState.RED  # => back where we started after exactly three transitions


def test_every_state_has_a_defined_next_state() -> None:
    for member in LightState:  # => iterate every enum member -- proves the table is total, not partial
        assert next_state(member) in LightState  # => must resolve to some valid member, never KeyError


# => Run: pytest -- Output: 2 passed
