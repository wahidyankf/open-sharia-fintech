"""Example 50: A Class-Attribute Instance Counter."""


class Dog:  # => begins the Dog class body
    population: int = 0  # => ONE shared counter, living on the class, not any instance

    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => stores name on this instance
        Dog.population += (
            1  # => mutates the CLASS attribute -- every instance sees the update
        )


Dog("Rex")  # => constructs one Dog, incrementing Dog.population to 1
Dog("Fido")  # => constructs a second Dog, incrementing Dog.population to 2
Dog("Max")  # => constructs a third Dog, incrementing Dog.population to 3
print(Dog.population)  # => reflects the total number of Dog() calls made so far
# => Output: 3
# => `Dog.population += 1` (mutating through the class name) updates the ONE shared counter every instance reads
