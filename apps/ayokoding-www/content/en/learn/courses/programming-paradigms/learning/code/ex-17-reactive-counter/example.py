"""Example 17: Reactive Counter."""

from collections.abc import Callable  # => Callable types every subscriber function stored below
# => a subscriber's signature is fixed: takes the new int value, returns nothing


class ObservableValue:  # => a minimal reactive primitive: a value that PUSHES updates on change
    def __init__(self, initial: int) -> None:  # => constructor seeds the starting value
        self._value: int = initial  # => the current value, hidden behind the property below
        self._subscribers: list[Callable[[int], None]] = []  # => everyone listening for changes

    def subscribe(self, fn: Callable[[int], None]) -> None:  # => register a listener
        self._subscribers.append(fn)  # => append -- does NOT call fn with the current value yet

    def set(self, new_value: int) -> None:  # => the ONLY way to change the value
        self._value = new_value  # => update the internal box
        for fn in self._subscribers:  # => PUSH: every subscriber is called automatically, right here
            fn(new_value)  # => no subscriber has to poll -- the value pushes the change to them


seen_by_subscriber: list[int] = []  # => where the subscriber below records what it observed
counter = ObservableValue(0)  # => start at 0
counter.subscribe(lambda v: seen_by_subscriber.append(v))  # => register a listener before any change

counter.set(1)  # => triggers the subscriber automatically
counter.set(2)  # => triggers it again
print(seen_by_subscriber)  # => the subscriber saw every update, in order, without polling
# => Output: [1, 2]
