"""Example 78: Auto-Registering Subclasses with __init_subclass__."""


class Shape:  # => begins the Shape class body
    registry: dict[
        str, type["Shape"]
    ] = {}  # => ONE shared registry, living on the base class

    def __init_subclass__(
        cls, **kwargs: object
    ) -> None:  # => fires automatically at SUBCLASS DEFINITION
        super().__init_subclass__(
            **kwargs
        )  # => cooperates with any other __init_subclass__ in the MRO
        Shape.registry[cls.__name__] = (
            cls  # => registers itself -- no manual call needed anywhere
        )


class Circle(Shape):  # => defining this class alone triggers __init_subclass__
    pass  # => an intentionally empty body


class Square(
    Shape
):  # => same here -- registration happens at class-definition time, not instantiation
    pass  # => an intentionally empty body


print(
    sorted(Shape.registry.keys())
)  # => both subclasses appear, with zero manual registration code
# => Output: ['Circle', 'Square']
# => `__init_subclass__` runs once per subclass, at the moment `class Circle(Shape):` finishes executing
