"""Example 68: Constructor-Injected Dependencies Enable Fakes in Tests."""


class RealClock:  # => begins the RealClock class body
    def now(self) -> str:  # => in real life this would call the system clock
        return "2026-07-14T00:00:00"  # => returns this value to the caller


class FakeClock:  # => a TEST DOUBLE -- no shared base class with RealClock, by design
    def now(self) -> str:  # => returns a fixed, predictable value instead
        return "1999-01-01T00:00:00"  # => returns this value to the caller


class Event:  # => begins the Event class body
    def __init__(
        self, clock: RealClock
    ) -> None:  # => the collaborator is INJECTED, not built inside
        self.clock = clock  # => stores clock on this instance

    def timestamp(self) -> str:  # => defines the timestamp() method
        return self.clock.now()  # => delegates to whichever clock was injected


real_event: Event = Event(RealClock())  # => constructs real_event
fake_event: Event = Event(FakeClock())  # type: ignore  # => duck typing lets a fake substitute cleanly
print(
    real_event.timestamp(), "|", fake_event.timestamp()
)  # => the SAME Event class, two results
# => Output: 2026-07-14T00:00:00 | 1999-01-01T00:00:00
# => Because `Event` never constructs its own clock, a test can inject `FakeClock()`
