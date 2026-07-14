"""Example 41: pytest verification for A Subclass Inherits Fields and Methods."""

from example import Cat


def test_subclass_inherits_base_init_field() -> None:
    c: Cat = Cat(
        "Whiskers"
    )  # => Cat has no __init__ of its own -- Animal's runs instead
    assert c.name == "Whiskers"


# => Run: pytest -- Output: 1 passed
