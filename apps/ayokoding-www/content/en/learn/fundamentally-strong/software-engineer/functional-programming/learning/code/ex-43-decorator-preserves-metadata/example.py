"""Example 43: functools.wraps Preserves __name__."""

from functools import wraps  # => wraps is the fix demonstrated in careful_decorator
from typing import Callable  # => Callable types both decorators below


def naive_decorator(
    fn: Callable[[], str],
) -> Callable[[], str]:  # => WITHOUT functools.wraps
    def wrapper() -> str:  # => the naive wrapper -- no metadata copied
        return fn()  # => forwards the call, nothing else

    return (
        wrapper  # => wrapper has its OWN __name__, "wrapper" -- fn's identity is lost
    )


def careful_decorator(
    fn: Callable[[], str],
) -> Callable[[], str]:  # => WITH functools.wraps
    @wraps(fn)  # => copies __name__, __doc__, and more from fn onto wrapper
    def wrapper() -> str:  # => the careful wrapper -- decorated with @wraps below
        return fn()  # => forwards the call, identical behavior to the naive version

    return wrapper  # => wrapper now REPORTS as if it were fn itself


@naive_decorator  # => applies the WITHOUT-wraps decorator
def greet_naive() -> str:  # => the function whose identity gets lost
    """Say hello, naively decorated."""  # => this docstring is LOST from greet_naive.__doc__ after decoration
    return "hello"  # => the actual greeting


@careful_decorator  # => applies the WITH-wraps decorator
def greet_careful() -> str:  # => the function whose identity survives decoration
    """Say hello, carefully decorated."""  # => this docstring IS preserved on greet_careful.__doc__
    return "hello"  # => the actual greeting


# => functools.wraps matters for debugging, introspection, and framework compatibility
print(
    greet_naive.__name__
)  # => Output: wrapper -- identity LOST, unhelpful in tracebacks/introspection
print(
    greet_careful.__name__
)  # => Output: greet_careful -- identity PRESERVED by functools.wraps
print(greet_careful.__doc__)  # => Output: Say hello, carefully decorated.
