"""Example 1: Define a Minimal Class."""


class Dog:  # => defines a new class named Dog -- a template, not yet an object
    pass  # => no fields or methods yet; a class body cannot be entirely empty in Python


d: Dog = Dog()  # => calling the class like a function CONSTRUCTS an instance
# => d is now a real object: the class Dog acted as a factory that built it
print(type(d) is Dog)  # => type(d) returns the exact class used to build d
# => Output: True
