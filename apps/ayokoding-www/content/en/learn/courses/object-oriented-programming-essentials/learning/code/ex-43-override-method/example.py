"""Example 43: Overriding a Method."""


class Animal:  # => begins the Animal class body
    def speak(self) -> str:  # => the base implementation
        return "..."  # => returns this value to the caller


class Cat(Animal):  # => Cat extends Animal
    def speak(self) -> str:  # => SAME name -- completely replaces the base version
        return "Meow"  # => returns this value to the caller


a: Animal = Animal()  # => constructs a
c: Cat = Cat()  # => constructs c
print(a.speak(), c.speak())  # => c.speak() runs Cat's version, not Animal's
# => Output: ... Meow
# => Defining a method with the same name as a base class method overrides it completely by default
