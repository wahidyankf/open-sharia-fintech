# => Use the standard-library helper required by this runnable model.
from itertools import cycle


# => Isolate the operation so its observable behavior can be checked.
def route(backends: list[str], count: int) -> list[str]:
    # Cycling assigns each equal-capacity backend one turn at a time.
    # => Initialize or update deterministic state used by this demonstration.
    choices = cycle(backends)
    # Taking a fixed request count makes the schedule inspectable.
    # => Return the observable result of this modeled operation.
    return [next(choices) for _ in range(count)]


# => Initialize or update deterministic state used by this demonstration.
result = route(["a", "b", "c"], 6)
# Equal turns demonstrate count distribution, not equal duration.
# => Check the promised observable behavior of the demonstration.
assert result == ["a", "b", "c", "a", "b", "c"]
# => Emit the final observable state for a direct run.
print(result)
