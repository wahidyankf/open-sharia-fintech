from typing import Final  # => typed relevance fixture

MEMORIES: Final[tuple[str, ...]] = (
    "uses Python",
    "likes tea",
    "timezone WIB",
)  # => stored facts
recalled: tuple[str, ...] = tuple(
    item for item in MEMORIES if "Python" in item
)  # => task-relevant filter
assert recalled == ("uses Python",)
print("PASS: memory-retrieval-policy")  # => irrelevant facts remain out
