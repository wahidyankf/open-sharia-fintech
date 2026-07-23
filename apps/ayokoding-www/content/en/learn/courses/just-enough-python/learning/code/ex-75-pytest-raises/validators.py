"""Example 75: a function that raises, under pytest.raises."""


def require_positive(value: int) -> int:  # => defines the function under test
    if value <= 0:  # => the condition this test exercises with value=0
        raise ValueError("value must be positive")  # => the behavior under test
    return value  # => only reached when value is > 0
