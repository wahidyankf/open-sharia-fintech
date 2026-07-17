"""Kata 9 (before): a hand-written and_then forgets to check for Err before calling the next step."""

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
    # SMELL: calls step() on result.value UNCONDITIONALLY -- never checks whether result is an Err first
    return step(result.value)  # type: ignore[union-attr]  # BUG: Err has no .value -- crashes on failure


def parse_positive(raw: str) -> Result[int, str]:
    n = int(raw)
    return Ok(n) if n > 0 else Err(f"{raw} is not positive")


def double_it(n: int) -> Result[int, str]:
    return Ok(n * 2)


first_step = parse_positive(
    "-5"
)  # this is a legitimate FAILURE, not a bug in parse_positive itself
final = and_then(
    first_step, double_it
)  # BUG: crashes with AttributeError instead of propagating Err
print(final)
