class SharedBucket:
    def __init__(self, tokens: int) -> None:
        # One object represents the atomic shared store used by every node.
        self.tokens = tokens

    def spend(self) -> bool:
        # A single decision point prevents each node from granting a local allowance.
        if self.tokens == 0:
            return False
        self.tokens -= 1
        return True


bucket = SharedBucket(2)
# Requests from distinct nodes consume the same two tokens.
assert [bucket.spend(), bucket.spend(), bucket.spend()] == [True, True, False]
print("shared limit enforced")
