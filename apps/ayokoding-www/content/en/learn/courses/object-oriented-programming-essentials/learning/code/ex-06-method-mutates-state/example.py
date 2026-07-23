"""Example 6: A Method That Mutates Instance State."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => starting value rename() below will overwrite

    def rename(
        self, new: str
    ) -> None:  # => mutates self in place; returns nothing (None)
        self.name = new  # => reassigns the SAME instance's name attribute


d: Dog = Dog("Rex")  # => constructs d
d.rename("Max")  # => mutates d.name -- there is no new Dog object here
print(d.name)  # => reads back the mutated value from the same instance
# => Output: Max
# => A method that mutates `self` and returns `None` is Python's normal shape for changing an object in place
