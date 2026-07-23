"""Example 46: isinstance Across a Hierarchy."""


class Animal:  # => begins the Animal class body
    pass  # => an intentionally empty body


class Cat(Animal):  # => Cat extends Animal
    pass  # => an intentionally empty body


c: Cat = Cat()  # => constructs c
print(isinstance(c, Cat))  # => True: c's own, exact class
# => Output: True
print(
    isinstance(c, Animal)
)  # => ALSO True: isinstance checks the WHOLE hierarchy, not exact type
# => Output: True
# => `isinstance` answers "is this object a Cat, or anything that IS-A Cat's ancestor"
