"""Example 1: pytest verification for Imperative Word Count."""

import runpy
from pathlib import Path
from typing import cast


def _run_example() -> dict[str, object]:
    # => runs example.py as __main__ and returns its module namespace for inspection
    path = Path(__file__).parent / "example.py"  # => locate the sibling script
    return runpy.run_path(str(path), run_name="__main__")  # => executes it, returns globals


def test_known_word_counts_match() -> None:
    ns = _run_example()  # => execute the imperative script once
    counts = cast("dict[str, int]", ns["counts"])  # => narrow the untyped namespace lookup
    assert counts["the"] == 3  # => "the" appears three times in the sample sentence
    assert counts["cat"] == 2  # => "cat" appears twice
    assert counts["sat"] == 1  # => every other word appears exactly once
    assert len(counts) == 6  # => six distinct words total


# => Run: pytest -- Output: 1 passed
