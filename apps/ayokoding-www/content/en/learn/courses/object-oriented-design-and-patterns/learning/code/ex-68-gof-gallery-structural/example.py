"""Example 68: GoF Gallery -- Structural Patterns.

co-32 (gof-pattern-gallery): a single-file tour of the five essential structural
patterns -- adapter (co-20), decorator (co-21), facade (co-22), composite (co-23),
and proxy (co-24) -- each wraps correctly, verified independently.
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from typing import Callable  # => Callable types the logging_decorator's wrapped function argument

# ============================================================
# 1. Adapter -- convert one interface into another a client expects
# ============================================================


class FahrenheitSensor:  # => the class being adapted -- exposes Fahrenheit only
    def read_fahrenheit(self) -> float:  # => the ONLY interface this class exposes
        return 98.6  # => a fixed sample reading, in Fahrenheit


class CelsiusAdapter:  # => converts FahrenheitSensor's interface into the one the client expects
    def __init__(self, sensor: FahrenheitSensor) -> None:  # => the constructor
        self._sensor = sensor  # => wraps the adapted object, held as a collaborator

    def read_celsius(self) -> float:  # => the interface the client actually wants
        return (self._sensor.read_fahrenheit() - 32) * 5 / 9  # => the conversion, hidden from the client


# ============================================================
# 2. Decorator -- wrap an object to add behavior without subclass explosion
# ============================================================


def logging_decorator(func: Callable[[str], str]) -> Callable[[str], str]:  # => wraps ANY str->str function
    def wrapped(message: str) -> str:  # => the replacement function returned in place of func
        result = func(message)  # => delegates to the wrapped function
        return f"[logged] {result}"  # => adds behavior around it, without editing func itself

    return wrapped  # => the decorator returns a NEW function, never mutates func in place


@logging_decorator  # => applies the wrapper at definition time -- greet IS wrapped from here on
def greet(name: str) -> str:  # => the wrapped function never knows it is being decorated
    return f"hello, {name}"  # => the original, undecorated behavior


# ============================================================
# 3. Facade -- one simplified entry point over a complex subsystem
# ============================================================


class Inventory:  # => one subsystem member
    def reserve(self, item: str) -> bool:  # => the reservation step, hidden inside the facade
        return True  # => stubbed: assume reservation always succeeds


class Payment:  # => another subsystem member
    def charge(self, amount: float) -> bool:  # => the charge step, hidden inside the facade
        return True  # => stubbed: assume payment always succeeds


class CheckoutFacade:  # => hides the sequencing of Inventory + Payment behind ONE call
    def __init__(self) -> None:  # => the constructor
        self._inventory = Inventory()  # => wires subsystem one internally
        self._payment = Payment()  # => wires subsystem two internally

    def checkout(self, item: str, amount: float) -> bool:  # => the caller makes ONE call
        return self._inventory.reserve(item) and self._payment.charge(amount)  # => sequencing hidden inside


# ============================================================
# 4. Composite -- treat individual objects and compositions uniformly
# ============================================================


class FileNode:  # => a leaf
    def __init__(self, size: int) -> None:  # => the constructor
        self.size = size  # => a leaf's own, fixed size

    def total_size(self) -> int:  # => the SHARED interface with DirectoryNode
        return self.size  # => a leaf's total IS its own size -- no recursion needed


class DirectoryNode:  # => a composite -- contains other FileNode or DirectoryNode children
    def __init__(self, children: list["FileNode | DirectoryNode"]) -> None:  # => the constructor
        self.children = children  # => a mix of leaves and/or nested composites, held uniformly

    def total_size(self) -> int:  # => the SAME interface as FileNode -- callers don't special-case leaf vs. group
        return sum(child.total_size() for child in self.children)  # => recurses uniformly


# ============================================================
# 5. Proxy -- a stand-in controlling access to a real subject
# ============================================================


class ExpensiveImage:  # => the "real subject", expensive to construct
    def __init__(self, path: str) -> None:  # => simulates a costly construction step
        self.path = path  # => stores the path on this instance
        self.loaded = True  # => simulates the expensive load happening at construction time


class LazyImageProxy:  # => the proxy -- defers construction until first access
    def __init__(self, path: str) -> None:  # => cheap: no ExpensiveImage built yet
        self._path = path  # => remembered so the real subject can be built later, on demand
        self._real: ExpensiveImage | None = None  # => not loaded yet

    def display(self) -> str:  # => the client-facing interface, identical shape to using ExpensiveImage directly
        if self._real is None:  # => only construct the real subject on FIRST access
            self._real = ExpensiveImage(self._path)  # => the expensive construction, deferred until now
        return f"displaying {self._real.path}"  # => every later call reuses the already-built real subject


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    adapter = CelsiusAdapter(FahrenheitSensor())  # => 1. adapter
    print(round(adapter.read_celsius(), 1))  # => the client reads Celsius, never touches Fahrenheit directly
    # => Output: 37.0

    print(greet("Ada"))  # => 2. decorator -- logging added without editing greet()
    # => Output: [logged] hello, Ada

    facade = CheckoutFacade()  # => 3. facade
    print(facade.checkout("Book", 12.5))  # => one call hides inventory + payment sequencing
    # => Output: True

    tree = DirectoryNode([FileNode(10), DirectoryNode([FileNode(5), FileNode(3)])])  # => 4. composite
    print(tree.total_size())  # => recursive total through ONE shared interface
    # => Output: 18

    proxy = LazyImageProxy("photo.png")  # => 5. proxy
    print(proxy._real is None)  # => not loaded yet -- proves laziness
    # => Output: True
    print(proxy.display())  # => triggers the load, on first access only
    # => Output: displaying photo.png
