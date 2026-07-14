"""Example 8: __repr__ for Debugging."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => stores name on this instance

    def __repr__(self) -> str:  # => called by print(), the REPL, and every traceback
        return f"Dog(name={self.name!r})"  # => !r formats name WITH quotes, like Python source


d: Dog = Dog("Rex")  # => constructs d
print(repr(d))  # => repr() calls __repr__ directly
# => Output: Dog(name='Rex')
# => `__repr__` controls how an object prints everywhere
