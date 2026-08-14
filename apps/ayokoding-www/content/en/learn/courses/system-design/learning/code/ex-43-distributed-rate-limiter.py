# => Group the state and behavior that model this design component.
class SharedBucket:
    # => Isolate the operation so its observable behavior can be checked.
    def __init__(self, tokens: int) -> None:
        # One object represents the atomic shared store used by every node.
        # => Initialize or update deterministic state used by this demonstration.
        self.tokens = tokens

    # => Isolate the operation so its observable behavior can be checked.
    def spend(self) -> bool:
        # A single decision point prevents each node from granting a local allowance.
        # => Choose the branch that models this design condition.
        if self.tokens == 0:
            # => Return the observable result of this modeled operation.
            return False
        # => Initialize or update deterministic state used by this demonstration.
        self.tokens -= 1
        # => Return the observable result of this modeled operation.
        return True


# => Initialize or update deterministic state used by this demonstration.
bucket = SharedBucket(2)
# Requests from distinct nodes consume the same two tokens.
# => Check the promised observable behavior of the demonstration.
assert [bucket.spend(), bucket.spend(), bucket.spend()] == [True, True, False]
# => Emit the final observable state for a direct run.
print("shared limit enforced")
