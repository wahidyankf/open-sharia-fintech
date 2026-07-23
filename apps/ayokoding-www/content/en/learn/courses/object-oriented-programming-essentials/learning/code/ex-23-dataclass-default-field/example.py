"""Example 23: A Dataclass Field with a Default Value."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass  # => generates boilerplate methods from the field list below
class Point:  # => begins the Point class body
    x: int  # => a required dataclass field, part of the generated __init__
    y: int  # => a required dataclass field, part of the generated __init__
    label: str = (
        ""  # => a default value -- fields with defaults must follow fields without one
    )


p: Point = Point(1, 2)  # => label omitted entirely
print(p.label == "")  # => confirms the default applied when the caller supplied nothing
# => Output: True
# => A dataclass default value works the same as any Python default argument
