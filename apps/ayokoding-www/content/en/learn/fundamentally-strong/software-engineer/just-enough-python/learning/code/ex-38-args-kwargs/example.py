"""Example 38: *args and **kwargs."""


def describe(*args: int, **kwargs: str) -> None:
    # args is a tuple, kwargs is a dict -- both are countable with len().
    print(len(args), len(kwargs))


describe(1, 2, 3, name="Ada", role="engineer")  # => 3 positional, 2 keyword
# => Output: 3 2
