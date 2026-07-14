"""Example 3: pytest verification for Define an Instance Method."""

from example import Dog


def test_bark_returns_woof() -> None:
    d: Dog = Dog("Rex")
    assert (
        d.bark() == "woof"
    )  # => calling the instance method returns its literal string


# => Run: pytest -- Output: 1 passed
