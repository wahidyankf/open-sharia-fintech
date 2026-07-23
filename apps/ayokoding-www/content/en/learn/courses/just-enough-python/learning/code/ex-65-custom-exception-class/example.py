"""Example 65: Custom Exception Class."""


# Subclassing Exception makes a NEW, specific error type.
class InvalidInputError(Exception):  # => defines a custom exception type
    """Raised when user-supplied input fails validation."""  # => shown by help() / tracebacks


# Defines parse_positive, which validates and converts raw.
def parse_positive(raw: str) -> int:
    value = int(raw)  # => converts raw to int; raises ValueError itself if not numeric
    if value <= 0:  # => the custom validation this function adds beyond int()
        raise InvalidInputError(f"expected a positive integer, got {value}")
        # => raises the custom exception with a descriptive message
    return value  # => only reached when value is > 0


try:  # => wraps the call so we can catch the custom exception below
    parse_positive("-5")  # => raises InvalidInputError("expected...got -5")
except InvalidInputError as err:  # => catches ONLY this custom type
    # => Output: rejected: expected a positive integer, got -5
    print(f"rejected: {err}")  # => str(err) is the message from InvalidInputError(...)
