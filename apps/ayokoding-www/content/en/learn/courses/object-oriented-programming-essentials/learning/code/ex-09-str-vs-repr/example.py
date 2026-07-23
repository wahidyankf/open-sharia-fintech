"""Example 9: str vs. repr."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => stores name on this instance

    def __repr__(self) -> str:  # => developer-facing, unambiguous
        return f"Dog(name={self.name!r})"  # => returns this value to the caller

    def __str__(self) -> str:  # => end-user-facing, readable prose
        return f"a dog named {self.name}"  # => deliberately different wording from __repr__


d: Dog = Dog("Rex")  # => constructs d
print(str(d), "|", repr(d))  # => str() prefers __str__; repr() always calls __repr__
# => Output: a dog named Rex | Dog(name='Rex')
# => `str(obj)` prefers `__str__` and falls back to `__repr__` only when `__str__` is absent
