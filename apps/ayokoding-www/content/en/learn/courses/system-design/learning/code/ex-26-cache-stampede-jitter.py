# => Use the standard-library helper required by this runnable model.
from random import Random


# => Isolate the operation so its observable behavior can be checked.
def deadlines(count: int, ttl: int, jitter: int) -> list[int]:
    # A seeded generator keeps this instructional schedule reproducible.
    # => Initialize or update deterministic state used by this demonstration.
    random = Random(7)
    # Each entry gets a bounded offset instead of one shared deadline.
    # => Return the observable result of this modeled operation.
    return [ttl + random.randint(-jitter, jitter) for _ in range(count)]


# => Initialize or update deterministic state used by this demonstration.
result = deadlines(20, 60, 5)
# More than one deadline proves refreshes are not perfectly synchronized.
# => Check the promised observable behavior of the demonstration.
assert len(set(result)) > 1 and all(55 <= deadline <= 65 for deadline in result)
# => Emit the final observable state for a direct run.
print(result)
