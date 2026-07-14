"""Example 7: A Default __init__ Argument."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str, legs: int = 4
    ) -> None:  # => legs defaults when omitted
        self.name = name  # => stores name on this instance
        self.legs = legs  # => uses the caller's value, or 4 if none was given


d: Dog = Dog("Rex")  # => legs omitted entirely -- Python supplies the default
print(d.legs)  # => confirms the default actually applied
# => Output: 4
# => `__init__` default arguments work exactly like default arguments on any function
