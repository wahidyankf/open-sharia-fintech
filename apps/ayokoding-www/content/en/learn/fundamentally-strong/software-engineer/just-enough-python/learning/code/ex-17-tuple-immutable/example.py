"""Example 17: Tuple Immutable."""

point: tuple[int, int] = (1, 2)  # => point is (1, 2) (type: tuple[int, int])
try:  # => wraps the mutation attempt so we can catch the expected error
    # Tuples are immutable -- item assignment always raises TypeError.
    point[0] = 9  # type: ignore[index]  # => raises TypeError before this line completes
except TypeError:  # => catches exactly the error tuples raise on item assignment
    print("immutable")  # => Output: immutable
