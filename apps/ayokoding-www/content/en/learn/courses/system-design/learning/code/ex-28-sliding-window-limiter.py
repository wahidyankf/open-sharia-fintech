# => Group the state and behavior that model this design component.
class SlidingWindow:
    # => Isolate the operation so its observable behavior can be checked.
    def __init__(self, limit: int, seconds: int) -> None:
        # Timestamps are injected to make the window boundary reproducible.
        # => Initialize or update deterministic state used by this demonstration.
        self.limit, self.seconds, self.events = limit, seconds, []

    # => Isolate the operation so its observable behavior can be checked.
    def allow(self, now: int) -> bool:
        # Drop events that are no longer inside the rolling interval.
        # => Initialize or update deterministic state used by this demonstration.
        self.events = [event for event in self.events if event > now - self.seconds]
        # => Choose the branch that models this design condition.
        if len(self.events) >= self.limit:
            # => Return the observable result of this modeled operation.
            return False
        # => Initialize or update deterministic state used by this demonstration.
        self.events.append(now)
        # => Return the observable result of this modeled operation.
        return True


# => Initialize or update deterministic state used by this demonstration.
window = SlidingWindow(2, 10)
# At t=10, the event at t=0 has expired while t=1 remains.
# => Check the promised observable behavior of the demonstration.
assert [window.allow(t) for t in (0, 1, 2, 10)] == [True, True, False, True]
# => Emit the final observable state for a direct run.
print(window.events)
