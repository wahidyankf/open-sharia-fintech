from typing import Final  # => typed tradeoff fixture

CHOICES: Final[set[str]] = {
    "truncate",
    "summarize",
}  # => explicit strategy alternatives
assert len(CHOICES) == 2
print("PASS: compare-compaction-strategies")  # => compare tradeoffs
