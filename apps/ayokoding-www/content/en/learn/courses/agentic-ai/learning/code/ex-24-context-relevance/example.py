from typing import Final  # => typed survey fixture

CONTEXT: Final[tuple[str, ...]] = (
    "relevant",
)  # => pruned context avoids transcript dump
assert CONTEXT == ("relevant",)  # => only task evidence remains
print("PASS: context-relevance")  # => credential-free result
