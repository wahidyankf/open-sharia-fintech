"""Example 28: pytest verification for self Is Just an Explicit First Argument."""

from example import Dog


def test_dot_call_equals_explicit_class_call() -> None:
    d: Dog = Dog("Rex")
    assert Dog.bark(d) == d.bark()  # => Dog.bark(d) is the desugared form of d.bark()


# => Run: pytest -- Output: 1 passed
