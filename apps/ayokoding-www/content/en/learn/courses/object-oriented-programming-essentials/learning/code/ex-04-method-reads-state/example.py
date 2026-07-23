"""Example 4: A Method That Reads Instance State."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => state greet() below will read back out

    def greet(
        self,
    ) -> str:  # => a method that builds its return value FROM self's own state
        return f"Hi, I'm {self.name}"  # => f-string interpolates self.name at call time


d: Dog = Dog("Rex")  # => constructs d
message: str = d.greet()  # => greet() reaches into self.name to build the sentence
print(message)  # => confirms the instance's own name flows through the method
# => Output: Hi, I'm Rex
# => A method's return value can be built entirely from `self`'s own fields, with no external arguments needed
