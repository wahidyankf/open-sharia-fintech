"""Example 75: Observer -- Memory Leak, Fixed With weakref.

co-26: the classic Observer memory leak -- a Subject holding STRONG references
to its observers keeps them alive forever, even after every other reference to
an observer is dropped, because the Subject itself is still a live referrer.
Switching the Subject's storage to `weakref.WeakSet` lets an unsubscribed,
otherwise-unreferenced observer be garbage-collected automatically.
"""

# => co-26 in one sentence: a Subject's own reference to an observer is a REAL reference, and real
# => references keep objects alive -- weakref.WeakSet trades that guarantee for automatic cleanup

from __future__ import annotations  # => defers type-hint evaluation, not strictly required here but kept for consistency

import gc  # => used to force collection deterministically for this demonstration
import weakref  # => weakref.WeakSet is the fix -- membership that does not keep members alive


class Event:  # => a minimal observer -- large in a real system, small here to keep the leak visible
    def __init__(self, name: str) -> None:  # => the constructor
        self.name = name  # => the only field, just enough to tell instances apart

    def notify(self, message: str) -> None:  # => the method any Subject would call on this observer
        pass  # => a real observer would react here; the leak does not depend on what notify() does


# => LeakySubject and WeakRefSubject expose the IDENTICAL public interface -- only storage differs
class LeakySubject:  # => co-26 ANTI-PATTERN: strong references keep every observer alive forever
    def __init__(self) -> None:  # => the constructor
        self._observers: list[Event] = []  # => a STRONG reference list -- the subject IS a live referrer

    def subscribe(self, observer: Event) -> None:  # => registers an observer, the leaky way
        self._observers.append(observer)  # => the subject now owns a strong reference

    def observer_count(self) -> int:  # => reports how many observers are still tracked
        return len(self._observers)  # => never shrinks on its own, even after the caller drops its reference


# => the fix is a ONE-LINE storage change (list -> WeakSet); subscribe() and observer_count() barely change
class WeakRefSubject:  # => co-26 FIX: a WeakSet does not keep its members alive
    def __init__(self) -> None:  # => the constructor
        self._observers: weakref.WeakSet[Event] = weakref.WeakSet()  # => weak references only

    def subscribe(self, observer: Event) -> None:  # => registers an observer, the fixed way
        self._observers.add(observer)  # => no strong reference created -- the subject does not keep this alive

    def observer_count(self) -> int:  # => reports how many observers are still tracked
        return len(self._observers)  # => automatically shrinks once an observer is garbage-collected elsewhere


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    # => both halves below follow the SAME script: construct, subscribe, drop the caller's reference, collect, count
    leaky = LeakySubject()  # => constructs the leaky implementation
    observer_a = Event("a")  # => the caller's own reference to a new observer
    leaky.subscribe(observer_a)  # => the subject now ALSO holds a strong reference
    del observer_a  # => the CALLER dropped its reference -- but the subject still holds one
    gc.collect()  # => forces collection so the leak is visible immediately, not just eventually
    print(leaky.observer_count())  # => LEAK: still 1 -- the strong reference kept it alive
    # => Output: 1
    # => the ONLY difference from here on is which Subject class is used -- same script, different result

    # => this second half mirrors the first exactly, line for line, except the subject class used
    fixed = WeakRefSubject()  # => constructs the fixed implementation
    observer_b = Event("b")  # => the caller's own reference to a new observer
    fixed.subscribe(observer_b)  # => the subject holds only a WEAK reference this time
    del observer_b  # => the caller dropped its only OTHER reference
    gc.collect()  # => nothing else references the Event, so it is collected
    print(fixed.observer_count())  # => FIXED: 0 -- weakref let it be garbage-collected
    # => Output: 0
    # => same subscribe/unsubscribe pattern, opposite outcome -- the storage type was the whole fix
