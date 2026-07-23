"""Example 50: raise ValueError."""


# raise stops execution immediately and propagates the exception up the call stack.
def parse_age(raw: str) -> int:  # => defines parse_age, converts and validates a string
    # int(raw) itself raises ValueError first if raw isn't numeric at all.
    age = int(raw)  # => converts raw to int
    if age < 0:  # => an extra validation check beyond what int() already does
        raise ValueError("bad input")  # => no except catches this here
    return age  # => only reached when age is >= 0


parse_age("-1")  # => uncaught -- crashes with a traceback, non-zero exit
