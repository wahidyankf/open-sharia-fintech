"""Example 58: pytest verification for A Dataclass Subclassing Another Dataclass."""

from example import Car


def test_combined_init_field_order_is_base_then_subclass() -> None:
    c: Car = Car(
        "Toyota", "Corolla", doors=4
    )  # => positional: make, model (base), doors (subclass)
    assert (c.make, c.model, c.doors) == ("Toyota", "Corolla", 4)


# => Run: pytest -- Output: 1 passed
