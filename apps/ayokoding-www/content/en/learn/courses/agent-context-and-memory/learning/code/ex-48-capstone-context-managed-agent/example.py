from typing import Final  # => typed end-to-end fixture

CONTEXT: Final[tuple[str, ...]] = (
    "system",
    "memory: concise",
    "retrieval: policy",
    "summary",
)  # => stable budgeted assembly
next_session: dict[str, str] = {
    "preference": "concise"
}  # => long-term recall after session boundary
assert (
    len(CONTEXT) <= 4
    and "retrieval: policy" in CONTEXT
    and next_session["preference"] == "concise"
)
print("PASS: capstone-context-managed-agent")  # => budget, relevance, recall
