from typing import Final  # => typed freshness fixture

MEMORY: Final[dict[str, tuple[int, str]]] = {
    "office": (2, "Jakarta")
}  # => corrected revision
candidate: tuple[int, str] = (1, "Bandung")  # => stale stored revision
chosen: str = max((candidate, MEMORY["office"]), key=lambda item: item[0])[
    1
]  # => newest wins
assert chosen == "Jakarta"
print("PASS: memory-staleness")  # => corrected value used
