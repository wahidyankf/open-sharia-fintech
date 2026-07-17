"""Example 77: Stacking Multiple Decorators and Reasoning About Order."""

from functools import (
    wraps,
)  # => preserves double's identity through both decorator layers
from typing import Callable  # => Callable types the logged decorator factory below

call_order: list[
    str
] = []  # => records the ACTUAL order decorators run in, top-to-bottom vs inside-out


def logged(
    label: str,
) -> Callable[[Callable[[int], int]], Callable[[int], int]]:  # => a decorator factory
    def decorator(
        fn: Callable[[int], int],
    ) -> Callable[[int], int]:  # => the actual decorator
        @wraps(fn)  # => preserves fn's identity through this layer
        def wrapper(
            x: int,
        ) -> int:  # => logs entry/exit around whatever fn this layer wraps
            call_order.append(f"{label} enter")  # => runs BEFORE the wrapped function
            result = fn(
                x
            )  # => calls the NEXT layer in (or the real function, if innermost)
            call_order.append(f"{label} exit")  # => runs AFTER the wrapped function
            return result  # => forwards the inner result unchanged

        return wrapper  # => decorator itself returns the logging wrapper

    return decorator  # => logged(label) itself returns the decorator


@logged(
    "outer"
)  # => applied SECOND -- wraps whatever @logged("inner") already produced
@logged("inner")  # => applied FIRST -- wraps the raw function directly
def double(x: int) -> int:  # => the innermost function, wrapped twice
    return x * 2  # => the actual computation, untouched by either decorator


result = double(5)  # => triggers BOTH wrapper layers, in a specific nesting order

# => decorator stacking is function composition wearing different syntax
print(result)  # => Output: 10
print(
    call_order
)  # => Output: ['outer enter', 'inner enter', 'inner exit', 'outer exit']
