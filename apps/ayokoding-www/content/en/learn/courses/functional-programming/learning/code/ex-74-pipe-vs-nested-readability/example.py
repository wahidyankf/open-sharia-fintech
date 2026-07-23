"""Example 74: A Deep pipe vs. Nested Calls on Real Data."""

from functools import reduce  # => reduce powers pipe's left-to-right fold
from typing import (
    Any,
    Callable,
)  # => Callable types the pipe helper below; Any types its dynamic arity


def pipe(
    *fns: Callable[..., Any],
) -> Callable[..., Any]:  # => reads TOP-TO-BOTTOM / LEFT-TO-RIGHT: first fn runs first
    def apply_step(
        acc: Any, fn: Callable[..., Any]
    ) -> Any:  # => named + typed -- one fold step, calls fn on acc
        return fn(acc)

    def piped(
        x: Any,
    ) -> Any:  # => named + typed -- an untyped lambda can't carry these annotations
        return reduce(apply_step, fns, x)  # => folds fns in ORDER, not reversed

    return piped  # => pipe itself returns the composed pipeline function


def strip_whitespace(text: str) -> str:  # => step 1
    return text.strip()  # => removes leading/trailing whitespace


def to_lowercase(text: str) -> str:  # => step 2
    return text.lower()  # => normalizes case


def split_words(text: str) -> list[str]:  # => step 3
    return text.split()  # => splits on any run of whitespace


def count_words(words: list[str]) -> int:  # => step 4
    return len(words)  # => the final count


raw = "  Hello  World  from   FUNCTIONAL Python  "  # => messy real-world input

nested_result = count_words(
    split_words(to_lowercase(strip_whitespace(raw)))
)  # => reads INSIDE-OUT
piped_result = pipe(strip_whitespace, to_lowercase, split_words, count_words)(
    raw
)  # => reads TOP-TO-BOTTOM

# => the exact same computation, argued for on READABILITY grounds alone
print(nested_result)  # => Output: 5
print(piped_result)  # => Output: 5
print(
    nested_result == piped_result
)  # => Output: True -- IDENTICAL computation, two different reading orders
