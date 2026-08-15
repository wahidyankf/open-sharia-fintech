class TokenBucket:
    def __init__(self, capacity: int) -> None:
        # Capacity bounds a burst before the service rejects more work.
        self.tokens = capacity

    def allow(self) -> bool:
        # The limiter makes overload an immediate, observable result.
        if self.tokens <= 0:
            return False
        self.tokens -= 1
        return True


bucket = TokenBucket(3)
# Three requests fit the stated capacity; a fourth is rejected.
assert [bucket.allow() for _ in range(4)] == [True, True, True, False]
print("capstone token bucket passed")
