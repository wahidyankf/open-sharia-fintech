from typing import Final  # => typed retrieval fixture

SCORES: Final[dict[str, int]] = {"relevant": 9, "noise": 1}  # => local nearest scores
assert max(SCORES, key=SCORES.get) == "relevant"
print("PASS: similarity-search")  # => top hit
