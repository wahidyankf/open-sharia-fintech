"""Example 5: pytest verification for Multiple Instances Stay Independent."""

from example import Dog


def test_instances_keep_separate_names() -> None:
    rex: Dog = Dog("Rex")
    fido: Dog = Dog("Fido")
    assert (
        rex.name == "Rex" and fido.name == "Fido"
    )  # => no cross-talk between the two objects


# => Run: pytest -- Output: 1 passed
