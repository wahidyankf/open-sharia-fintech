"""Example 65: Anti-Pattern -- Singleton Abuse.

co-34 (anti-pattern recognition) + co-19 (singleton and its costs): a singleton used
as a shared mutable counter is hidden global coupling -- any test that runs before
another can silently leak state into it, because nothing in either test's signature
reveals the dependency exists.
"""

from __future__ import annotations  # => defers type-hint evaluation, letting RequestCounter reference itself


# => the singleton pattern itself: __new__ ensures only ONE instance is ever created, globally
class RequestCounter:  # => a classic singleton: one shared instance, reachable globally
    # => the Optional sentinel pattern: None means "not constructed yet", the class itself means "constructed"
    _instance: "RequestCounter | None" = None  # => the one shared instance, or None before first use

    def __new__(cls) -> "RequestCounter":  # => __new__ is overridden so every RequestCounter() returns the SAME object
        if cls._instance is None:  # => first call: create the one instance
            cls._instance = super().__new__(cls)  # => allocate it exactly once
            # => count is set dynamically here, never declared in the class body -- static checkers cannot see it
            cls._instance.count = 0  # type: ignore[attr-defined]  # => initialize state on the shared instance
        return cls._instance  # => every subsequent call returns this SAME object, not a new one

    # => every call to increment(), from ANYWHERE in the program, mutates this one shared counter
    def increment(self) -> int:  # => mutates the ONE shared instance's state
        # => the `# type: ignore[attr-defined]` markers exist because count is never declared as a class field
        self.count += 1  # type: ignore[attr-defined]  # => hidden global mutation -- no caller passed this in
        return self.count  # type: ignore[attr-defined]


# => neither handle_request_a nor handle_request_b takes a counter parameter -- the coupling is invisible
def handle_request_a() -> int:  # => neither function's SIGNATURE reveals it depends on RequestCounter
    counter = RequestCounter()  # => silently reaches for the global singleton
    return counter.increment()  # => mutates shared state as a side effect


# => this function looks completely independent of handle_request_a, yet secretly shares its state
def handle_request_b() -> int:  # => a completely unrelated-looking function...
    counter = RequestCounter()  # => ...that happens to share state with handle_request_a via the singleton
    return counter.increment()  # => whichever function runs first determines the other's starting count


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    # NOTE: resetting _instance here is itself evidence of the cost -- production code has no clean reset hook
    # => contrast with dependency injection: a passed-in counter would need no such manual reset ritual
    RequestCounter._instance = None  # => manual reset required before every isolated demonstration
    # => without the manual reset on the line above, this count would carry over from any earlier run
    print(handle_request_a())  # => first call anywhere: count becomes 1
    # => Output: 1
    print(handle_request_b())  # => a DIFFERENT function, yet it sees count=2 -- hidden coupling via the singleton
    # => Output: 2
    # => the defining trait of a singleton: two separate construction calls, one identity
    print(RequestCounter() is RequestCounter())  # => confirms both calls returned the exact same object
    # => Output: True
