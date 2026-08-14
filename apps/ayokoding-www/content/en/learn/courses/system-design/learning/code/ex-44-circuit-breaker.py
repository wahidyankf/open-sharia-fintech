# => Group the state and behavior that model this design component.
class CircuitBreaker:
    # => Isolate the operation so its observable behavior can be checked.
    def __init__(self, threshold: int) -> None:
        # The threshold makes repeated failures an explicit policy choice.
        # => Initialize or update deterministic state used by this demonstration.
        self.threshold, self.failures, self.state = threshold, 0, "closed"

    # => Isolate the operation so its observable behavior can be checked.
    def call(self, succeeds: bool) -> str:
        # An open breaker rejects quickly rather than spending more dependency time.
        # => Choose the branch that models this design condition.
        if self.state == "open":
            # => Return the observable result of this modeled operation.
            return "rejected"
        # => Choose the branch that models this design condition.
        if not succeeds:
            # => Initialize or update deterministic state used by this demonstration.
            self.failures += 1
            # => Choose the branch that models this design condition.
            if self.failures >= self.threshold:
                # => Initialize or update deterministic state used by this demonstration.
                self.state = "open"
            # => Return the observable result of this modeled operation.
            return "failed"
        # => Initialize or update deterministic state used by this demonstration.
        self.failures = 0
        # => Return the observable result of this modeled operation.
        return "ok"


# => Initialize or update deterministic state used by this demonstration.
breaker = CircuitBreaker(2)
# The second failure trips the breaker; a later call receives a fast rejection.
# => Check the promised observable behavior of the demonstration.
assert [breaker.call(False), breaker.call(False), breaker.call(True)] == [
    # => Initialize or update deterministic state used by this demonstration.
    "failed",
    # => Initialize or update deterministic state used by this demonstration.
    "failed",
    # => Initialize or update deterministic state used by this demonstration.
    "rejected",
    # => Initialize or update deterministic state used by this demonstration.
]
# => Emit the final observable state for a direct run.
print(breaker.state)
