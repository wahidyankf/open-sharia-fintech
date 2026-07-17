"""Example 75: TSP -- Brute Force (Optimal, Slow) vs Nearest-Neighbor (Fast, Not Optimal)."""

# The Traveling Salesman Problem (co-28) is NP-hard: no known algorithm
# solves it in polynomial time, and brute force explores ALL (n-1)!
# orderings to guarantee optimality. A GREEDY heuristic like nearest-neighbor
# runs in polynomial time but offers NO optimality guarantee -- this example
# proves that gap empirically on one small, concrete instance.
import itertools
import math

Point = tuple[float, float]  # => an (x, y) coordinate


def dist(a: Point, b: Point) -> float:  # => straight-line (Euclidean) distance
    return math.hypot(a[0] - b[0], a[1] - b[1])


def tour_length(order: tuple[int, ...], cities: list[Point]) -> float:
    total = 0.0
    n = len(order)
    for i in range(
        n
    ):  # => sums edge (i -> i+1), wrapping the LAST city back to the first
        total += dist(cities[order[i]], cities[order[(i + 1) % n]])
    return total


def brute_force_tsp(cities: list[Point]) -> tuple[tuple[int, ...], float]:
    # => tries EVERY possible ordering -- guaranteed optimal, but O(n!) work
    n = len(cities)
    best_order: tuple[int, ...] | None = None
    best_length: float | None = None
    for perm in itertools.permutations(
        range(1, n)
    ):  # => fixes city 0 as the start -- a cyclic tour has no unique "first" city anyway
        order = (0,) + perm
        length = tour_length(order, cities)
        if best_length is None or length < best_length:
            best_length = length  # => tracks the shortest tour seen so far
            best_order = order
    assert (
        best_order is not None and best_length is not None
    )  # => n >= 1 guarantees a result
    return best_order, best_length


def nearest_neighbor_tsp(cities: list[Point]) -> tuple[list[int], float]:
    # => GREEDILY hops to the closest unvisited city -- O(n^2), no backtracking
    n = len(cities)
    visited = [False] * n
    order = [0]  # => starts at city 0, same fixed start as brute force
    visited[0] = True
    for _ in range(n - 1):
        last = order[-1]
        best_j: int | None = None
        best_d: float | None = None
        for j in range(n):
            if not visited[j]:  # => only considers cities NOT yet in the tour
                d = dist(cities[last], cities[j])
                if best_d is None or d < best_d:
                    best_d = d  # => the CLOSEST unvisited city so far
                    best_j = j
        assert best_j is not None  # => at least one unvisited city remains here
        order.append(best_j)
        visited[best_j] = True
    return order, tour_length(tuple(order), cities)


# A hand-picked 7-city instance where greedy nearest-neighbor genuinely gets
# TRAPPED: an early greedy hop leaves a far-away city stranded for last,
# forcing an expensive final edge that a globally optimal tour avoids.
cities: list[Point] = [
    (4.6, 5.2),
    (6.4, 6.0),
    (5.6, 6.2),
    (9.4, 5.1),
    (4.3, 7.2),
    (2.4, 3.0),
    (9.8, 5.2),
]

brute_order, brute_length = brute_force_tsp(cities)
nn_order, nn_length = nearest_neighbor_tsp(cities)
print(round(brute_length, 2))  # => Output: 18.81 -- the PROVABLY shortest possible tour
print(
    round(nn_length, 2)
)  # => Output: 22.19 -- greedy's tour, longer but found MUCH faster

assert brute_length <= nn_length  # => brute force NEVER loses -- it tries every option
assert (
    nn_length > brute_length * 1.1
)  # => confirms the heuristic is genuinely SUBOPTIMAL here
assert (
    math.factorial(len(cities) - 1) == 720
)  # => brute force's search space: 6! orderings for 7 cities
print("ex-75 OK")  # => Output: ex-75 OK
