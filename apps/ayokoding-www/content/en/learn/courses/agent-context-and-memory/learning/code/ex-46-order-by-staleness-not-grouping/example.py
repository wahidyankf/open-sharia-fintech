from typing import Final  # => typed cache-order fixture

STABLE: Final[tuple[str, ...]] = (
    "system",
    "tools",
    "corpus",
)  # => reusable prefix components
first: str = "|".join(STABLE + ("turn-1", "result-1"))
second: str = "|".join(STABLE + ("turn-2", "result-2"))  # => volatile tail
assert first.split("|", 3)[:3] == second.split("|", 3)[:3]
print("PASS: order-by-staleness-not-grouping")  # => byte-identical prefix
