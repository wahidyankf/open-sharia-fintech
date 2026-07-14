"""Example 58: A Dataclass Subclassing Another Dataclass."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass  # => generates boilerplate methods from the field list below
class Vehicle:  # => begins the Vehicle class body
    make: str  # => a required dataclass field, part of the generated __init__
    model: str  # => a required dataclass field, part of the generated __init__


@dataclass  # => generates boilerplate methods from the field list below
class Car(Vehicle):  # => inherits make/model, adds its OWN field after them
    doors: int = (
        4  # => new fields must come AFTER inherited fields in the generated __init__
    )


c: Car = Car(
    "Toyota", "Corolla", doors=4
)  # => positional order: make, model, THEN doors
print(
    c.make, c.model, c.doors
)  # => confirms all three fields, from both classes, are set
# => Output: Toyota Corolla 4
# => `@dataclass` inheritance concatenates field lists, base class first, subclass second
