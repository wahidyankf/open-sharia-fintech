"""Example 67: A Lazy-Loading Descriptor Defers Its Query Until First Attribute Access."""  # => this concept

import dataclasses  # => the loaded parent object the descriptor attaches to
from typing import Any  # => __get__ must return whatever the loader function produces


class LazyAttribute:  # => co-21: a descriptor that loads its value ONLY on first access, not at construction
    def __init__(self, loader: Any) -> None:  # => `loader` is a zero-arg callable, run at most once
        self._loader = loader  # => the deferred computation -- NOT run yet, just stored
        self._loaded = False  # => co-21: tracks whether the loader has already run
        self._value: Any = None  # => holds the result ONCE the loader has run

    def __get__(self, instance: object, owner: type) -> Any:  # => called EVERY time the attribute is read
        if not self._loaded:  # => co-21: the FIRST access -- nothing has run yet
            self._value = self._loader()  # => runs the deferred computation NOW, not before
            self._loaded = True  # => marks it run -- future accesses skip straight to the cached value
        return self._value  # => the loaded (or previously-cached) value


call_count = 0  # => co-21: instrumented so this example can PROVE the loader deferred, not eager


def expensive_query() -> str:  # => simulates a real database query, counted every time it actually runs
    global call_count  # => mutates the module-level counter above
    call_count += 1  # => co-21: counts EVERY time this function actually executes
    return "loaded-orders"  # => the "query result" this lazy attribute eventually returns


@dataclasses.dataclass  # => a domain object with ONE lazy-loaded attribute
class Customer:  # => the parent object -- construction must NOT trigger the lazy load
    name: str  # => an ordinary, eagerly-set column
    orders = LazyAttribute(expensive_query)  # => co-21: NOT called yet -- just wired up as a class attribute


customer = Customer(name="Alice")  # => construction complete -- orders has NOT been accessed yet
assert call_count == 0  # => co-21: the loader has NOT run -- deferred past construction entirely
value = customer.orders  # => co-21: FIRST access -- THIS is what triggers expensive_query()
assert call_count == 1  # => confirms the loader ran EXACTLY once, triggered by the access above
assert value == "loaded-orders"  # => the returned value matches what the loader produced
print(call_count)  # => Output: 1
