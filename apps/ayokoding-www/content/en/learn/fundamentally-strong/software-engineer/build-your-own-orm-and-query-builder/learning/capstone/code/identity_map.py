# pyright: strict
"""Capstone: identity_map.py -- a per-session {(table, pk): object} cache (co-13), backed by
a weakref.WeakValueDictionary (co-14) so an unreferenced loaded object can be garbage
collected instead of leaking for the session's entire lifetime.
"""

import weakref
from typing import TypeVar

T = TypeVar("T")


class IdentityMap:
    def __init__(self) -> None:  # => starts empty -- nothing cached before any load
        self._cache: "weakref.WeakValueDictionary[tuple[str, int], object]" = weakref.WeakValueDictionary()  # => co-14: entries disappear on their own once nothing else references the object

    def get(self, table: str, pk: int, cls: type[T]) -> T | None:  # => co-13: keyed by (table, pk)
        found = self._cache.get((table, pk))  # => a cache MISS returns None, exactly like dict.get
        if found is None:
            return None
        assert isinstance(found, cls)  # => narrows `object` back to T for the caller, checked at runtime
        return found

    def put(self, table: str, pk: int, obj: object) -> None:  # => co-13: registers BEFORE the caller uses it
        self._cache[(table, pk)] = obj  # => co-14: a WEAK reference -- does not keep obj alive by itself


if __name__ == "__main__":  # => guards against running the demo on `import identity_map`
    import dataclasses
    import gc

    @dataclasses.dataclass
    class Customer:
        id: int
        name: str

    identity_map = IdentityMap()
    alice = Customer(id=1, name="Alice")
    identity_map.put("customer", 1, alice)
    same = identity_map.get("customer", 1, Customer)
    print(same is alice)  # => Output: True
    assert same is alice  # => co-13: the exact same object, not a second equal copy

    del alice, same
    gc.collect()  # => forces collection so the drop below is deterministic
    print(identity_map.get("customer", 1, Customer))  # => Output: None
    assert identity_map.get("customer", 1, Customer) is None  # => co-14: the entry dropped, nothing leaked
