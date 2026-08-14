class CircuitBreaker:
    def __init__(self, threshold: int) -> None:
        # The threshold makes repeated failures an explicit policy choice.
        self.threshold, self.failures, self.state = threshold, 0, "closed"

    def call(self, succeeds: bool) -> str:
        # An open breaker rejects quickly rather than spending more dependency time.
        if self.state == "open":
            return "rejected"
        if not succeeds:
            self.failures += 1
            if self.failures >= self.threshold:
                self.state = "open"
            return "failed"
        self.failures = 0
        return "ok"


breaker = CircuitBreaker(2)
# The second failure trips the breaker; a later call receives a fast rejection.
assert [breaker.call(False), breaker.call(False), breaker.call(True)] == [
    "failed",
    "failed",
    "rejected",
]
print(breaker.state)
