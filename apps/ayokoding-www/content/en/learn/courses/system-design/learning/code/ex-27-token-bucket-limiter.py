# => Group the state and behavior that model this design component.
class TokenBucket:
    # => Isolate the operation so its observable behavior can be checked.
    def __init__(self, capacity: int) -> None:
        # This deterministic demo starts full and omits clock-based refills.
        # => Initialize or update deterministic state used by this demonstration.
        self.tokens = capacity

    # => Isolate the operation so its observable behavior can be checked.
    def allow(self) -> bool:
        # Refuse immediately once the shared capacity is spent.
        # => Choose the branch that models this design condition.
        if self.tokens == 0:
            # => Return the observable result of this modeled operation.
            return False
        # => Initialize or update deterministic state used by this demonstration.
        self.tokens -= 1
        # => Return the observable result of this modeled operation.
        return True


# => Initialize or update deterministic state used by this demonstration.
bucket = TokenBucket(2)
# Two admissions consume the burst; the third sees a fast rejection.
# => Check the promised observable behavior of the demonstration.
assert [bucket.allow() for _ in range(3)] == [True, True, False]
# => Emit the final observable state for a direct run.
print("bucket enforced")
