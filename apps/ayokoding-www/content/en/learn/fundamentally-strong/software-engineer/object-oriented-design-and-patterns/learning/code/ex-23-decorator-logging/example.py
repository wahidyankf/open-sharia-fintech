"""Example 23: Decorator: Log a Service Call Without Editing It."""

from functools import wraps  # => wraps preserves the wrapped function's name and docstring
from typing import Callable  # => Callable types the function log_calls wraps

LOG: list[str] = []  # => the shared record every decorated call appends to


def log_calls(
    fn: Callable[[float], str],
    # => the decorator FACTORY -- takes the original function, returns a wrapped one
) -> Callable[[float], str]:  # => returns a function with the SAME signature as fn
    @wraps(fn)  # => keeps fn.__name__ intact for debugging and introspection
    def wrapper(amount: float) -> str:  # => the wrapper -- runs BEFORE and AFTER fn
        LOG.append(f"calling {fn.__name__} with {amount}")  # => logs BEFORE the real call
        result: str = fn(amount)  # => the ORIGINAL behavior, completely unedited
        LOG.append(f"{fn.__name__} returned {result}")  # => logs AFTER the real call
        return result  # => returns the original result, unchanged

    return wrapper  # => this wrapper REPLACES the original function at the call site


@log_calls  # => the ONLY edit needed -- charge()'s own body never changes
def charge(amount: float) -> str:  # => the ORIGINAL service method, untouched internally
    return f"charged {amount}"  # => the real, honest business logic


result: str = charge(50.0)  # => calls the WRAPPED version transparently
print(result)  # => the business result is identical to calling charge() undecorated
print(LOG)  # => confirms logging happened, entirely OUTSIDE charge()'s own body
# => Output: charged 50.0
# => ['calling charge with 50.0', 'charge returned charged 50.0']
# => `charge`'s source code has zero logging statements -- `@log_calls` added the behavior from outside
