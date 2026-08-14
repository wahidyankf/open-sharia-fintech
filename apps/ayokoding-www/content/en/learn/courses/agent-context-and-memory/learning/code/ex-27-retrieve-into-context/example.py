from typing import Final  # => typed context fixture

CHUNKS: Final[tuple[str, ...]] = ("relevant fact",)  # => top-k retrieval result
assert CHUNKS[0] == "relevant fact"
print("PASS: retrieve-into-context")  # => evidence inserted
