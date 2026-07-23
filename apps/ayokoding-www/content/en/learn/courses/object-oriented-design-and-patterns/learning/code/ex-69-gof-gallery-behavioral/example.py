"""Example 69: GoF Gallery -- Behavioral Patterns.

co-32 (gof-pattern-gallery): a single-file tour of seven essential behavioral
patterns -- strategy (co-25), observer (co-26), command (co-27), template method
(co-28), state (co-29), iterator (co-30), and chain of responsibility (co-31) --
each dispatches correctly, verified independently.
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from abc import ABC, abstractmethod  # => builds the template-method, state, and chain-of-responsibility bases
from typing import Callable, Iterator  # => Callable types strategies/observers, Iterator types the custom collection

# ============================================================
# 1. Strategy -- interchangeable algorithms behind one interface
# ============================================================


def by_length(word: str) -> int:  # => one strategy
    return len(word)  # => a plain function IS a strategy -- no class hierarchy required


def sort_words(words: list[str], key: Callable[[str], int]) -> list[str]:  # => the dispatcher, takes a strategy
    return sorted(words, key=key)  # => the strategy decides HOW to compare


# ============================================================
# 2. Observer -- subjects notify subscribers without knowing them concretely
# ============================================================


class Publisher:  # => the subject
    def __init__(self) -> None:  # => the constructor
        self._subscribers: list[Callable[[str], None]] = []  # => knows only that subscribers are callables

    def subscribe(self, handler: Callable[[str], None]) -> None:  # => adding a subscriber needs no publisher edit
        self._subscribers.append(handler)  # => grows the list, nothing else

    def publish(self, message: str) -> None:  # => notifies every subscriber, without knowing what they do
        for handler in self._subscribers:  # => visits every registered subscriber, in order
            handler(message)  # => the subject never knows what a handler does with the message


# ============================================================
# 3. Command -- reify a request as an object with execute/undo
# ============================================================


class AddTextCommand:  # => a request, turned into an object
    def __init__(self, document: list[str], text: str) -> None:  # => the constructor
        self.document = document  # => the receiver this command acts on
        self.text = text  # => remembers WHAT it appended, needed later to undo

    def execute(self) -> None:  # => performs the request
        self.document.append(self.text)  # => the forward action

    def undo(self) -> None:  # => reverses the request
        self.document.remove(self.text)  # => the reverse action, mirroring execute() exactly


# ============================================================
# 4. Template Method -- a base defines the skeleton, subclasses fill steps
# ============================================================


class ReportBase(ABC):  # => defines the FIXED skeleton
    def run(self) -> str:  # => the shared flow, defined exactly once
        return f"[{self.header()}] {self.body()} [{self.footer()}]"  # => calls the varying steps in a fixed order

    @abstractmethod  # => forces every subclass to fill this ONE varying step
    def body(self) -> str:  # => the ONLY step subclasses must fill
        raise NotImplementedError  # => abstract method body, never actually executed

    def header(self) -> str:  # => a step with a sensible default, overridable
        return "REPORT"  # => the shared default, used unless a subclass overrides it

    def footer(self) -> str:  # => another step with a sensible default
        return "END"  # => the shared default, used unless a subclass overrides it


class SalesReport(ReportBase):  # => fills only the varying step
    def body(self) -> str:  # => overrides the ONE required step -- header() and footer() stay default
        return "sales: 42 units"  # => the only thing SalesReport ever needs to supply


# ============================================================
# 5. State -- represent states as objects so transitions are explicit
# ============================================================


class TrafficLightState(ABC):  # => the shared state interface every concrete light color implements
    @abstractmethod  # => forces every concrete state to define its own legal next transition
    def next(self) -> "TrafficLightState":  # => returns the NEXT legal state
        raise NotImplementedError  # => abstract method body, never actually executed


class Red(TrafficLightState):  # => one concrete state object, not a boolean flag
    def next(self) -> TrafficLightState:  # => encodes red's ONE legal transition
        return Green()  # => red -> green is the only legal move


class Green(TrafficLightState):  # => a second concrete state object
    def next(self) -> TrafficLightState:  # => encodes green's ONE legal transition
        return Yellow()  # => green -> yellow


class Yellow(TrafficLightState):  # => a third concrete state object, completing the cycle
    def next(self) -> TrafficLightState:  # => encodes yellow's ONE legal transition
        return Red()  # => yellow -> red, completing the cycle


# ============================================================
# 6. Iterator -- expose sequential access without revealing representation
# ============================================================


class EvenNumbers:  # => a custom collection with hidden internal representation
    def __init__(self, upper_bound: int) -> None:  # => the constructor
        self._upper_bound = upper_bound  # => the only internal state -- callers never see this directly

    def __iter__(self) -> Iterator[int]:  # => the iterator protocol -- callers just use a for loop
        current = 0  # => the iteration cursor, private to this generator
        while current < self._upper_bound:  # => stops once the bound is reached
            yield current  # => lazily yields the next even number
            current += 2  # => advances the cursor by 2, staying on even numbers


# ============================================================
# 7. Chain of Responsibility -- pass a request along handlers until one handles it
# ============================================================


class Handler(ABC):  # => the shared link interface every tier in the chain implements
    def __init__(self) -> None:  # => the constructor
        self._next: "Handler | None" = None  # => no successor linked yet -- set_next() wires it later

    def set_next(self, handler: "Handler") -> "Handler":  # => links this handler to the next one in the chain
        self._next = handler  # => stores the successor link
        return handler  # => returned so calls can chain: a.set_next(b).set_next(c)

    def handle(self, level: int) -> str:  # => tries to handle, or passes along
        if self.can_handle(level):  # => asks the CONCRETE subclass whether it can resolve this level
            return self.resolve(level)  # => yes -- resolve it here, the chain stops
        if self._next is not None:  # => not handled here -- pass to the next link
            return self._next.handle(level)  # => delegates, recursively, to the next handler in the chain
        return "UNHANDLED"  # => fell off the end of the chain

    @abstractmethod  # => forces every concrete handler to define its own eligibility check
    def can_handle(self, level: int) -> bool:
        raise NotImplementedError  # => abstract method body, never actually executed

    @abstractmethod  # => forces every concrete handler to define its own resolution
    def resolve(self, level: int) -> str:
        raise NotImplementedError  # => abstract method body, never actually executed


class TierOneSupport(Handler):  # => the FIRST link in the chain
    def can_handle(self, level: int) -> bool:  # => tier 1's own eligibility rule
        return level <= 1  # => only handles the lowest severity levels

    def resolve(self, level: int) -> str:  # => tier 1's own resolution
        return "resolved by tier 1"


class TierTwoSupport(Handler):  # => the SECOND link in the chain
    def can_handle(self, level: int) -> bool:  # => tier 2's own eligibility rule
        return level <= 2  # => handles what tier 1 could not

    def resolve(self, level: int) -> str:  # => tier 2's own resolution
        return "resolved by tier 2"


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    print(sort_words(["banana", "kiwi", "fig"], key=by_length))  # => 1. strategy
    # => Output: ['fig', 'kiwi', 'banana']

    events: list[str] = []  # => the list the observer's handler will append into
    publisher = Publisher()  # => 2. observer
    publisher.subscribe(lambda msg: events.append(msg.upper()))  # => registers a handler, no Publisher edit needed
    publisher.publish("news")  # => notifies every subscriber, this one included
    print(events)
    # => Output: ['NEWS']

    doc: list[str] = []  # => the receiver AddTextCommand will mutate
    cmd = AddTextCommand(doc, "hello")  # => 3. command
    cmd.execute()  # => performs the request: appends "hello" to doc
    cmd.undo()  # => reverses the SAME request: removes "hello" from doc
    print(doc)
    # => Output: []

    print(SalesReport().run())  # => 4. template method
    # => Output: [REPORT] sales: 42 units [END]

    light: TrafficLightState = Red()  # => 5. state
    light = light.next()  # => transitions via a method call, never an if/elif on a string or int flag
    print(type(light).__name__)
    # => Output: Green

    print(list(EvenNumbers(10)))  # => 6. iterator
    # => Output: [0, 2, 4, 6, 8]

    tier_one: Handler = TierOneSupport()  # => 7. chain of responsibility
    tier_two = TierTwoSupport()  # => the second link, not yet wired into the chain
    tier_one.set_next(tier_two)  # => wires tier_one -> tier_two
    print(tier_one.handle(2))  # => tier 1 can't handle level 2, passes to tier 2
    # => Output: resolved by tier 2
