# => Use the standard-library helper required by this runnable model.
from time import monotonic

# => Use the standard-library helper required by this runnable model.
from typing import Optional


# => Group the state and behavior that model this design component.
class TtlCache:
    # => Isolate the operation so its observable behavior can be checked.
    def __init__(self) -> None:
        # Store both value and the deadline that defines freshness.
        # => Initialize or update deterministic state used by this demonstration.
        self.values: dict[str, tuple[str, float]] = {}

    # => Isolate the operation so its observable behavior can be checked.
    def put(self, key: str, value: str, ttl: float) -> None:
        # Monotonic time avoids wall-clock adjustments changing expiry.
        # => Initialize or update deterministic state used by this demonstration.
        self.values[key] = (value, monotonic() + ttl)

    # => Isolate the operation so its observable behavior can be checked.
    def get(self, key: str) -> Optional[str]:
        # An expired entry is a miss rather than a stale success.
        # => Initialize or update deterministic state used by this demonstration.
        value = self.values.get(key)
        # => Return the observable result of this modeled operation.
        return value[0] if value and value[1] > monotonic() else None


# => Initialize or update deterministic state used by this demonstration.
cache = TtlCache()
# => Initialize or update deterministic state used by this demonstration.
cache.put("fresh", "value", 10)
# => Initialize or update deterministic state used by this demonstration.
cache.put("old", "value", -1)
# => Check the promised observable behavior of the demonstration.
assert cache.get("fresh") == "value" and cache.get("old") is None
# => Emit the final observable state for a direct run.
print("expiry checked")
