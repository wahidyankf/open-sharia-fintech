"""Example 44: Calling super() Inside an Override."""


class Animal:  # => begins the Animal class body
    def speak(self) -> str:  # => defines the speak() method
        return "..."  # => returns this value to the caller


class Cat(Animal):  # => Cat extends Animal
    def speak(self) -> str:  # => defines the speak() method
        base: str = (
            super().speak()
        )  # => explicitly invokes Animal's own implementation first
        return f"Meow (base said: {base})"  # => AUGMENTS the base result instead of discarding it


c: Cat = Cat()  # => constructs c
print(c.speak())  # => combines both the base and the override's own contribution
# => Output: Meow (base said: ...)
# => An override is not forced to choose between "replace entirely" (Example 43) and "reuse entirely" (Example 41)
