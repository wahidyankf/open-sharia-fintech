from typing import Final  # => typed chunking fixture

RECALL: Final[dict[str, int]] = {"small": 2, "large": 1}  # => local strategy outcomes
assert RECALL["small"] > RECALL["large"]
print("PASS: chunking-strategy-contrast")  # => compare recall
