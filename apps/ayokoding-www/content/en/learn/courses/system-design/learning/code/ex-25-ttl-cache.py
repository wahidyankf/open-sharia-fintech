from time import monotonic
from typing import Optional


class TtlCache:
    def __init__(self) -> None:
        # Store both value and the deadline that defines freshness.
        self.values: dict[str, tuple[str, float]] = {}

    def put(self, key: str, value: str, ttl: float) -> None:
        # Monotonic time avoids wall-clock adjustments changing expiry.
        self.values[key] = (value, monotonic() + ttl)

    def get(self, key: str) -> Optional[str]:
        # An expired entry is a miss rather than a stale success.
        value = self.values.get(key)
        return value[0] if value and value[1] > monotonic() else None


cache = TtlCache()
cache.put("fresh", "value", 10)
cache.put("old", "value", -1)
assert cache.get("fresh") == "value" and cache.get("old") is None
print("expiry checked")
