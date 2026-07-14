"""Example 42: Chaining Construction with super().__init__()."""


class Animal:  # => begins the Animal class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => set by the BASE class's own __init__


class Cat(Animal):  # => Cat extends Animal
    def __init__(
        self, name: str, indoor: bool
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        super().__init__(name)  # => explicitly runs Animal.__init__ first
        self.indoor = indoor  # => THEN adds the subclass's own field


c: Cat = Cat("Whiskers", indoor=True)  # => constructs c
print(c.name, c.indoor)  # => both the base field and the subclass field are set
# => Output: Whiskers True
# => `super().__init__(...)` is how a subclass reuses the base class's construction logic instead of duplicating it
