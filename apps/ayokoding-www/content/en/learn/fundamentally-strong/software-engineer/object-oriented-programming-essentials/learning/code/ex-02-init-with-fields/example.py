"""Example 2: Initialize Fields in __init__."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => runs automatically when Dog(...) is called
        self.name = name  # => stores the argument on THIS instance's own namespace


d: Dog = Dog("Rex")  # => __init__ runs immediately, setting d.name to "Rex"
print(d.name)  # => reads the instance attribute set inside __init__
# => Output: Rex
# => `__init__(self, ...)` is where constructor arguments become instance state, via plain `self.field = value` assignment
