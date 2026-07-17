"""Example 79: Decorator -- functools Decorator vs. a GoF Class Decorator.

co-21: Python's `@decorator` syntax and the GoF Decorator pattern solve the
SAME problem -- adding cross-cutting behavior without editing the wrapped
object's source -- but at different granularities. A `functools`-based
FUNCTION decorator wraps a single callable; a GoF-style CLASS decorator wraps
an OBJECT and forwards the rest of its interface, useful when you need to wrap
something that is not a bare function (e.g. an object with several methods).
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

import functools  # => functools.wraps preserves the wrapped function's identity through decoration
from typing import Callable, Protocol  # => Callable types the function decorator, Protocol types the class one


# ============================================================
# Pythonic native: a functools-based FUNCTION decorator
# ============================================================


# => log_calls returns a brand-new function -- add() below never has its own source code touched
def log_calls(func: Callable[..., float]) -> Callable[..., float]:  # => wraps a single callable
    @functools.wraps(func)  # => preserves func.__name__/__doc__ -- good decorator hygiene
    def wrapper(*args: float, **kwargs: float) -> float:  # => the replacement function returned in place of func
        result = func(*args, **kwargs)  # => delegates to the wrapped function, unchanged
        wrapper.calls.append((args, result))  # type: ignore[attr-defined]  # => records every call, cross-cutting
        return result  # => the SAME result the wrapped function would have returned

    wrapper.calls = []  # type: ignore[attr-defined]  # => a log attached to the wrapper itself
    return wrapper  # => a NEW callable, never mutates func in place


@log_calls  # => the native, idiomatic way to add cross-cutting behavior to ONE function
def add(a: float, b: float) -> float:  # => the wrapped function, unaware it is being decorated
    return a + b  # => the original, undecorated behavior


# ============================================================
# GoF style: a CLASS decorator wrapping a whole object, forwarding its interface
# ============================================================


class Calculator(Protocol):  # => the interface a GoF class decorator must preserve
    def compute(self, a: float, b: float) -> float: ...  # => the ONE method any Calculator must provide


class PlainAdder:  # => the object being decorated -- has state and MULTIPLE potential methods, not just one function
    def compute(self, a: float, b: float) -> float:  # => satisfies Calculator structurally
        return a + b  # => the original, undecorated behavior


class LoggingCalculatorDecorator:  # => co-21: GoF Decorator -- wraps an OBJECT, forwards its interface
    def __init__(self, wrapped: Calculator) -> None:  # => the constructor
        self._wrapped = wrapped  # => the object being decorated, held as a collaborator
        self.calls: list[tuple[float, float, float]] = []  # => a log attached to this decorator instance

    def compute(self, a: float, b: float) -> float:  # => forwards the SAME interface Calculator declares
        result = self._wrapped.compute(a, b)  # => delegates to the wrapped object -- same interface preserved
        self.calls.append((a, b, result))  # => the cross-cutting behavior: logging every call
        return result  # => the SAME result the wrapped object would have returned


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    print(add(2, 3))  # => the function decorator runs transparently
    # => Output: 5
    print(add.calls)  # type: ignore[attr-defined]  # => cross-cutting logging attached without touching add()'s own body
    # => Output: [((2, 3), 5)]

    decorated_calculator = LoggingCalculatorDecorator(PlainAdder())  # => wraps a WHOLE object, not a bare function
    print(decorated_calculator.compute(4, 5))  # => the class decorator also runs transparently
    # => Output: 9
    print(decorated_calculator.calls)  # => same cross-cutting idea, applied to a whole OBJECT instead of one function
    # => Output: [(4, 5, 9)]
