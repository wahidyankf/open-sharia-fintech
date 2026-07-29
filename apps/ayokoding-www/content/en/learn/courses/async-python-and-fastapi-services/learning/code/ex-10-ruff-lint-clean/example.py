"""Example 10: Linting and Formatting Clean with ruff.

This module IS the lint-clean artifact. Run: ruff check example.py && ruff format --check example.py
-> zero findings. (co-08)
"""

from collections.abc import Sequence  # => the precise typed alias for "a sequence of ints"


def double_each(values: Sequence[int]) -> list[int]:  # => fully typed signature -- ruff and pyright both like it
    # => a list comprehension is idiomatic, short, and lint-clean -- no manual loop index needed (co-08)
    return [value * 2 for value in values]  # => one transformed value per input, in order


if __name__ == "__main__":  # => run directly to confirm behaviour
    result = double_each([1, 2, 3])  # => transform a small sequence
    print(result)  # => Output: [2, 4, 6]
