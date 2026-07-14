"""Example 45: Polymorphic Dispatch Over a Mixed List."""


class Animal:  # => begins the Animal class body
    def speak(self) -> str:  # => defines the speak() method
        return "..."  # => returns this value to the caller


class Cat(Animal):  # => Cat extends Animal
    def speak(self) -> str:  # => defines the speak() method
        return "Meow"  # => returns this value to the caller


class Dog(Animal):  # => Dog extends Animal
    def speak(self) -> str:  # => defines the speak() method
        return "Woof"  # => returns this value to the caller


animals: list[Animal] = [
    Cat(),
    Dog(),
    Animal(),
]  # => ONE list, THREE different runtime types
sounds: list[str] = [
    a.speak() for a in animals
]  # => same .speak() call-site for every element
print(sounds)  # => each element dispatched to its OWN class's implementation
# => Output: ['Meow', 'Woof', '...']
# => `[a.speak() for a in animals]` never branches on `type(a)` anywhere
