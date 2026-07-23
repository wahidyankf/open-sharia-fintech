"""Example 68: __set_name__ Lets a Descriptor Cache Per-Instance, Not Per-Descriptor."""  # => this concept

from typing import Any, Callable  # => the loader's signature and the descriptor's generic value type


class LazyAttribute:  # => co-21: caches on the INSTANCE via __set_name__, not on the descriptor itself
    def __init__(self, loader: Callable[[], Any]) -> None:  # => `loader` is a zero-arg callable
        self._loader = loader  # => the deferred computation, stored but not yet run
        self._private_name = ""  # => placeholder, OVERWRITTEN by __set_name__ before any real use

    def __set_name__(self, owner: type, name: str) -> None:  # => co-21: called ONCE, at class body execution
        self._private_name = f"_lazy_{name}"  # => e.g. "orders" becomes "_lazy_orders" -- unique per attribute

    def __get__(self, instance: object, owner: type) -> Any:  # => called EVERY time the attribute is read
        if not hasattr(instance, self._private_name):  # => co-21: THIS instance has never loaded it before
            setattr(instance, self._private_name, self._loader())  # => stores the result ON the instance itself
        return getattr(instance, self._private_name)  # => co-21: per-instance cache, not shared across instances


call_log: list[str] = []  # => co-21: records WHICH instance triggered a load, proving isolation


def make_loader(label: str) -> Callable[[], str]:  # => builds a loader that records its own label when it runs
    def loader() -> str:  # => the actual deferred computation
        call_log.append(label)  # => co-21: proves per-instance isolation -- each instance loads independently
        return f"orders-for-{label}"  # => a value distinguishable per instance

    return loader  # => a fresh closure, capturing THIS call's label


class Customer:  # => a domain object with a lazy attribute shared at the CLASS level
    orders = LazyAttribute(make_loader("shared-descriptor"))  # => co-21: ONE descriptor, MANY instances


alice = Customer()  # => instance one -- has its OWN private cache slot via __set_name__
bob = Customer()  # => instance two -- a SEPARATE private cache slot, same descriptor object
_ = alice.orders  # => triggers alice's OWN load -- writes to alice's private attribute, not bob's
_ = bob.orders  # => triggers bob's OWN load -- independently, because __set_name__ scoped it per-instance
assert call_log == ["shared-descriptor", "shared-descriptor"]  # => co-21: BOTH loaded, independently, once each
assert alice.orders == bob.orders  # => same loader, same label -- but two SEPARATE per-instance cache entries
print(len(call_log))  # => Output: 2
