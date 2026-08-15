from typing import Final  # => typed composition fixture

SOURCES: Final[set[str]] = {
    "system",
    "task",
    "history",
    "retrieval",
    "tools",
}  # => diagram nodes
assert len(SOURCES) == 5
print("PASS: context-composition-diagram")  # => all compete
