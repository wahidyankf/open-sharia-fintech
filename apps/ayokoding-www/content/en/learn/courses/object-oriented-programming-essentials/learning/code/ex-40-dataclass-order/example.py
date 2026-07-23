"""Example 40: order=True Adds Field-Tuple Comparisons."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(order=True)  # => generates __lt__, __le__, __gt__, __ge__ from field ORDER
class Point:  # => begins the Point class body
    x: int  # => a required dataclass field, part of the generated __init__
    y: int  # => comparisons check x first, then y -- exactly like tuple comparison


points: list[Point] = [
    Point(2, 1),
    Point(1, 5),
    Point(1, 2),
]  # => deliberately out of order
points.sort()  # => sort() uses the generated __lt__ under the hood
print(points)  # => sorted by (x, y) as a tuple: (1,2) < (1,5) < (2,1)
# => Output: [Point(x=1, y=2), Point(x=1, y=5), Point(x=2, y=1)]
# => `order=True` makes instances directly sortable with `list.sort()` or `sorted()`
