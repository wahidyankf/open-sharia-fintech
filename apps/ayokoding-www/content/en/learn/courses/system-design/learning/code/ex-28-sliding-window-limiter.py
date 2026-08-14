class SlidingWindow:
    def __init__(self, limit: int, seconds: int) -> None:
        # Timestamps are injected to make the window boundary reproducible.
        self.limit, self.seconds, self.events = limit, seconds, []

    def allow(self, now: int) -> bool:
        # Drop events that are no longer inside the rolling interval.
        self.events = [event for event in self.events if event > now - self.seconds]
        if len(self.events) >= self.limit:
            return False
        self.events.append(now)
        return True


window = SlidingWindow(2, 10)
# At t=10, the event at t=0 has expired while t=1 remains.
assert [window.allow(t) for t in (0, 1, 2, 10)] == [True, True, False, True]
print(window.events)
