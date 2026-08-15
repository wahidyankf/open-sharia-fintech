from typing import Final  # => typed context fixture

PARTS: Final[tuple[str, ...]] = (
    "system",
    "task",
    "memory",
    "retrieval",
    "history",
)  # => assembled components
context: tuple[str, ...] = PARTS[:4]  # => budgeted rolling history exclusion
assert len(context) <= 4 and "memory" in context
print("PASS: full-context-pipeline")  # => fits and stays relevant
