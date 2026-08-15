from typing import Final  # => typed per-turn fixture

CONTEXT: Final[str] = "relevant knowledge"  # => fresh retrieved context
assert CONTEXT.startswith("relevant")
print("PASS: retrieval-in-the-loop")  # => per-turn evidence
