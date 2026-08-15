from typing import Final  # => typed relevance fixture

SCORES: Final[dict[str, int]] = {"relevant": 9, "stale": 1}  # => ranking input
assert max(SCORES, key=SCORES.get) == "relevant"
print("PASS: relevance-scored-inclusion")  # => select evidence
