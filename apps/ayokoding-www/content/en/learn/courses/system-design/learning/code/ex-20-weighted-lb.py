# => Use the standard-library helper required by this runnable model.
from itertools import cycle


# => Isolate the operation so its observable behavior can be checked.
def weighted_route(weights: dict[str, int], count: int) -> list[str]:
    # Repeat a backend once per declared capacity unit.
    # => Initialize or update deterministic state used by this demonstration.
    slots = [backend for backend, weight in weights.items() for _ in range(weight)]
    # Cycling slots yields the requested capacity ratio.
    # => Initialize or update deterministic state used by this demonstration.
    chooser = cycle(slots)
    # => Return the observable result of this modeled operation.
    return [next(chooser) for _ in range(count)]


# => Initialize or update deterministic state used by this demonstration.
result = weighted_route({"small": 1, "large": 2}, 6)
# The larger backend receives twice as many scheduled requests.
# => Check the promised observable behavior of the demonstration.
assert result.count("large") == 4 and result.count("small") == 2
# => Emit the final observable state for a direct run.
print(result)
