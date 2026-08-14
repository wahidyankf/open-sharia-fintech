from typing import Final  # => typed resolver fixture

CLAIMS: Final[tuple[tuple[str, int], ...]] = (
    ("weekly", 1),
    ("daily", 2),
)  # => fact plus confidence
resolved: str = max(CLAIMS, key=lambda claim: claim[1])[
    0
]  # => highest-confidence policy
assert resolved == "daily"
print("PASS: memory-conflict-resolution")  # => defined resolution
