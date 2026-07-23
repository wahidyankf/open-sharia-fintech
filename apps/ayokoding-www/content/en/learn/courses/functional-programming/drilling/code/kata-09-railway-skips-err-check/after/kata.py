"""Kata 9 (after): fix -- and_then checks the variant BEFORE calling the next step, short-circuiting on Err."""

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E


Result = Ok[T] | Err[E]


def and_then(
    result: Result[T, str], step: Callable[[T], Result[U, str]]
) -> Result[U, str]:
    match (
        result
    ):  # => checks the variant FIRST, exactly once, before ever calling step()
        case Ok(value=v):
            return step(v)  # => only reachable when result actually succeeded
        case Err(error=e):
            return Err(e)  # => short-circuits -- step() is never called on a failure


def parse_positive(raw: str) -> Result[int, str]:
    n = int(raw)
    return Ok(n) if n > 0 else Err(f"{raw} is not positive")


def double_it(n: int) -> Result[int, str]:
    return Ok(n * 2)


first_step = parse_positive("-5")
final = and_then(
    first_step, double_it
)  # correctly short-circuits, double_it is never called
print(final)
