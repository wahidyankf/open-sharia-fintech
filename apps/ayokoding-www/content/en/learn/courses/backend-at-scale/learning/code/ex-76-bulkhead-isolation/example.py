# pyright: strict
"""Example 76: Bulkhead -- isolate resource pools. (co-39)

A bulkhead partitions resources into ISOLATED pools so a failure or saturation
in one does not sink the others. Here pool A and pool B are separate; when
pool A is fully saturated (all its permits held), pool B still serves its own
calls. The bulkhead pattern was introduced by Michael Nygard in Release It!.
"""

from dataclasses import dataclass  # => a small typed record for one isolated pool


@dataclass  # => co-39: one isolated resource pool with a fixed permit count
class Pool:
    name: str  # => the pool's label
    permits: int  # => max concurrent in-flight calls this pool allows
    in_use: int = 0  # => currently held permits
    rejected: int = 0  # => calls turned away because the pool was full

    def acquire(self) -> bool:  # => take a permit if one is available
        if self.in_use >= self.permits:  # => co-39: this pool is saturated
            self.rejected += 1  # => count the rejection
            return False  # => caller must wait/fail
        self.in_use += 1  # => hold a permit
        return True  # => acquired

    def release(self) -> None:  # => return a permit
        self.in_use = max(0, self.in_use - 1)  # => never negative


pool_a = Pool("A", permits=2)  # => co-39: pool A allows 2 concurrent calls
pool_b = Pool("B", permits=2)  # => co-39: pool B is SEPARATE -- A's saturation does not touch it

# Saturate pool A fully.
pool_a.acquire()  # => A in_use=1
pool_a.acquire()  # => A in_use=2 (now full)
a_rejected = pool_a.acquire()  # => co-39: pool A is saturated -> this call is rejected
print(f"pool A saturated, 3rd call acquired: {a_rejected}, rejected count: {pool_a.rejected}")  # => Output: False, 1

# Pool B is ISOLATED -- it still serves even though pool A is full.
b_served = pool_b.acquire()  # => co-39: pool B has its OWN permits -> unaffected by A
print(f"pool B serves while A is saturated: {b_served}")  # => Output: True

assert a_rejected is False and pool_a.rejected == 1  # => co-39: A's saturation rejected the overflow
assert b_served is True  # => co-39: the bulkhead kept B serving despite A being full
