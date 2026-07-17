"""Example 39: pytest verification for Cycling States via the State Pattern."""

from example import TrafficLight


def test_next_cycles_red_green_yellow_red() -> None:
    light: TrafficLight = TrafficLight()
    assert light.state.name() == "red"  # => starting state
    assert light.next() == "green"  # => red -> green
    assert light.next() == "yellow"  # => green -> yellow
    assert light.next() == "red"  # => yellow -> red, cycle closes


# => Run: pytest -- Output: 1 passed
