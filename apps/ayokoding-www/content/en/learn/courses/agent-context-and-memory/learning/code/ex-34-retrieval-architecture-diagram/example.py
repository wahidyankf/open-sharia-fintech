from typing import Final  # => typed pipeline fixture

STAGES: Final[tuple[str, ...]] = (
    "chunk",
    "embed",
    "store",
    "retrieve",
    "rerank",
    "context",
)  # => RAG flow
assert len(STAGES) == 6
print("PASS: retrieval-architecture-diagram")  # => all stages shown
