class TokenBucket:
    def __init__(self, capacity: int) -> None:
        # This deterministic demo starts full and omits clock-based refills.
        self.tokens = capacity

    def allow(self) -> bool:
        # Refuse immediately once the shared capacity is spent.
        if self.tokens == 0:
            return False
        self.tokens -= 1
        return True


bucket = TokenBucket(2)
# Two admissions consume the burst; the third sees a fast rejection.
assert [bucket.allow() for _ in range(3)] == [True, True, False]
print("bucket enforced")
