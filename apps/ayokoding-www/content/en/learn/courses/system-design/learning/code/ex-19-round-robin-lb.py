from itertools import cycle


def route(backends: list[str], count: int) -> list[str]:
    # Cycling assigns each equal-capacity backend one turn at a time.
    choices = cycle(backends)
    # Taking a fixed request count makes the schedule inspectable.
    return [next(choices) for _ in range(count)]


result = route(["a", "b", "c"], 6)
# Equal turns demonstrate count distribution, not equal duration.
assert result == ["a", "b", "c", "a", "b", "c"]
print(result)
