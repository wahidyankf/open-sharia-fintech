from itertools import cycle


def weighted_route(weights: dict[str, int], count: int) -> list[str]:
    # Repeat a backend once per declared capacity unit.
    slots = [backend for backend, weight in weights.items() for _ in range(weight)]
    # Cycling slots yields the requested capacity ratio.
    chooser = cycle(slots)
    return [next(chooser) for _ in range(count)]


result = weighted_route({"small": 1, "large": 2}, 6)
# The larger backend receives twice as many scheduled requests.
assert result.count("large") == 4 and result.count("small") == 2
print(result)
