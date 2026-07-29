"""Example 50: The ruff and pyright Gate.

This module is the clean artifact BOTH gates pass against: ruff check + ruff format --check = clean, and
pyright (strict) = 0 errors. Run: ruff check example.py && ruff format --check example.py && pyright example.py.
(co-08, co-09)
"""

from collections.abc import Mapping  # => a precise typed alias -- ruff prefers it over dict[str, V]


def summarize(counts: Mapping[str, int]) -> dict[str, int]:  # => fully typed in AND out (co-09)
    # => a dict comprehension is idiomatic, lint-clean, and typed -- no manual accumulator needed (co-08)
    return {key: value for key, value in counts.items() if value > 0}  # => drop zero-count entries


if __name__ == "__main__":  # => run directly to confirm behaviour
    result = summarize({"a": 1, "b": 0, "c": 3})  # => one entry dropped
    print(result)  # => Output: {'a': 1, 'c': 3}
