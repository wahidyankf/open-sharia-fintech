from typing import Final  # => typed audit fixture

RECORDS: Final[tuple[str, ...]] = (
    "fresh: preference",
    "stale: office",
    "private: api_key",
)  # => memory inventory
findings: tuple[str, ...] = tuple(
    item for item in RECORDS if not item.startswith("fresh")
)  # => audit filter
assert len(findings) == 2
print("PASS: memory-audit")  # => stale and private reported
