# => Use the standard-library helper required by this runnable model.
from collections import OrderedDict

# => Use the standard-library helper required by this runnable model.
from typing import Optional


# => Group the state and behavior that model this design component.
class LruCache:
    # => Isolate the operation so its observable behavior can be checked.
    def __init__(self, capacity: int) -> None:
        # Ordered keys let the least-recent item stay at the front.
        # => Initialize or update deterministic state used by this demonstration.
        self.capacity, self.values = capacity, OrderedDict()

    # => Isolate the operation so its observable behavior can be checked.
    def get(self, key: str) -> Optional[str]:
        # A read refreshes recency by moving the key to the end.
        # => Initialize or update deterministic state used by this demonstration.
        value = self.values.pop(key, None)
        # => Choose the branch that models this design condition.
        if value is not None:
            # => Initialize or update deterministic state used by this demonstration.
            self.values[key] = value
        # => Return the observable result of this modeled operation.
        return value

    # => Isolate the operation so its observable behavior can be checked.
    def put(self, key: str, value: str) -> None:
        # Replace existing keys before deciding whether capacity is exceeded.
        # => Initialize or update deterministic state used by this demonstration.
        self.values.pop(key, None)
        # => Initialize or update deterministic state used by this demonstration.
        self.values[key] = value
        # => Choose the branch that models this design condition.
        if len(self.values) > self.capacity:
            # The front is the least-recently-used entry.
            # => Initialize or update deterministic state used by this demonstration.
            self.values.popitem(last=False)


# => Initialize or update deterministic state used by this demonstration.
cache = LruCache(2)
# => Initialize or update deterministic state used by this demonstration.
cache.put("a", "A")
# => Initialize or update deterministic state used by this demonstration.
cache.put("b", "B")
# => Initialize or update deterministic state used by this demonstration.
cache.get("a")
# => Initialize or update deterministic state used by this demonstration.
cache.put("c", "C")
# => Check the promised observable behavior of the demonstration.
assert cache.get("b") is None and cache.get("a") == "A"
# => Emit the final observable state for a direct run.
print(list(cache.values))
