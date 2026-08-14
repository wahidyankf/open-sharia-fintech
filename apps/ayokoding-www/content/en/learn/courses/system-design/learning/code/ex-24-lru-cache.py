from collections import OrderedDict
from typing import Optional


class LruCache:
    def __init__(self, capacity: int) -> None:
        # Ordered keys let the least-recent item stay at the front.
        self.capacity, self.values = capacity, OrderedDict()

    def get(self, key: str) -> Optional[str]:
        # A read refreshes recency by moving the key to the end.
        value = self.values.pop(key, None)
        if value is not None:
            self.values[key] = value
        return value

    def put(self, key: str, value: str) -> None:
        # Replace existing keys before deciding whether capacity is exceeded.
        self.values.pop(key, None)
        self.values[key] = value
        if len(self.values) > self.capacity:
            # The front is the least-recently-used entry.
            self.values.popitem(last=False)


cache = LruCache(2)
cache.put("a", "A")
cache.put("b", "B")
cache.get("a")
cache.put("c", "C")
assert cache.get("b") is None and cache.get("a") == "A"
print(list(cache.values))
