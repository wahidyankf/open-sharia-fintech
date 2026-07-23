"""Example 75: TSP -- Brute Force (Optimal, Slow) vs Nearest-Neighbor (Fast, Not Optimal)."""

# The Traveling Salesman Problem (co-28) is NP-hard: no known algorithm
# solves it in polynomial time, and brute force explores ALL (n-1)!
# orderings to guarantee optimality. A GREEDY heuristic like nearest-neighbor
# runs in polynomial time but offers NO optimality guarantee -- this example
# proves that gap empirically on one small, concrete instance.
import itertools  # => generates every permutation for the brute-force search
import math  # => hypot() for Euclidean distance, factorial() for the search-space size

# => (x, y) coordinates in an arbitrary 2D plane, used for straight-line distance
Point = tuple[float, float]  # => an (x, y) coordinate


def dist(a: Point, b: Point) -> float:  # => straight-line (Euclidean) distance
    return math.hypot(a[0] - b[0], a[1] - b[1])  # => the distance formula, built in


def tour_length(  # => sums every consecutive edge, wrapping the tour back to the start
    order: tuple[int, ...], cities: list[Point]
) -> float:  # => total tour distance
    total = 0.0  # => running sum of edge lengths
    n = len(order)  # => the number of cities in this tour
    for i in range(  # => opens the edge-summing loop
        n  # => one edge per city in the tour
    ):  # => sums edge (i -> i+1), wrapping the LAST city back to the first
        total += dist(  # => opens the edge-distance addition
            cities[order[i]], cities[order[(i + 1) % n]]
        )  # => this edge's length
    return total  # => the complete tour's total distance


def brute_force_tsp(  # => tries EVERY ordering to guarantee the optimal tour
    cities: list[Point],
) -> tuple[tuple[int, ...], float]:  # => O(n!) exhaustive
    # => tries EVERY possible ordering -- guaranteed optimal, but O(n!) work
    n = len(cities)  # => the number of cities to visit
    best_order: tuple[int, ...] | None = None  # => the shortest ordering found so far
    best_length: float | None = None  # => that ordering's total length
    for perm in itertools.permutations(  # => opens the every-ordering search
        range(1, n)  # => every OTHER city, in every possible order
    ):  # => fixes city 0 as the start -- a cyclic tour has no unique "first" city anyway
        order = (0,) + perm  # => reattaches the fixed starting city
        length = tour_length(order, cities)  # => this candidate ordering's total length
        if (  # => opens the new-shortest-tour check
            best_length is None or length < best_length
        ):  # => a strictly shorter tour was found
            best_length = length  # => tracks the shortest tour seen so far
            best_order = order  # => and the ordering that produced it
    assert (  # => opens the at-least-one-permutation sanity check
        best_order is not None
        and best_length is not None  # => at least one permutation ran
    )  # => n >= 1 guarantees a result
    return best_order, best_length  # => the PROVABLY optimal tour and its length


def nearest_neighbor_tsp(  # => greedily hops to the closest unvisited city each step
    cities: list[Point],
) -> tuple[list[int], float]:  # => O(n^2) greedy
    # => GREEDILY hops to the closest unvisited city -- O(n^2), no backtracking
    n = len(cities)  # => the number of cities to visit
    visited = [False] * n  # => tracks which cities are already in the tour
    order = [0]  # => starts at city 0, same fixed start as brute force
    visited[0] = True  # => marks the starting city as visited
    for _ in range(n - 1):  # => adds one more city to the tour on each iteration
        last = order[-1]  # => the most recently added city
        best_j: int | None = None  # => the closest unvisited city found so far
        best_d: float | None = None  # => that city's distance from `last`
        for j in range(n):  # => scans every city as a candidate next hop
            if not visited[j]:  # => only considers cities NOT yet in the tour
                d = dist(cities[last], cities[j])  # => distance from the current city
                if best_d is None or d < best_d:  # => a strictly closer unvisited city
                    best_d = d  # => the CLOSEST unvisited city so far
                    best_j = j  # => and which city that is
        assert best_j is not None  # => at least one unvisited city remains here
        order.append(best_j)  # => greedily commits to the closest city
        visited[best_j] = True  # => marks it as visited
    return order, tour_length(tuple(order), cities)  # => the greedy tour and its length


# A hand-picked 7-city instance where greedy nearest-neighbor genuinely gets
# TRAPPED: an early greedy hop leaves a far-away city stranded for last,
# forcing an expensive final edge that a globally optimal tour avoids.
cities: list[Point] = [  # => opens the 7-city coordinate literal
    (4.6, 5.2),  # => city 0 -- the fixed starting point
    (6.4, 6.0),  # => city 1
    (5.6, 6.2),  # => city 2
    (9.4, 5.1),  # => city 3
    (4.3, 7.2),  # => city 4
    (2.4, 3.0),  # => city 5
    (9.8, 5.2),  # => city 6 -- the far-away trap for greedy
]  # => closes the coordinate literal

brute_order, brute_length = brute_force_tsp(cities)  # => the guaranteed-optimal tour
nn_order, nn_length = nearest_neighbor_tsp(cities)  # => the fast, non-optimal tour
print(round(brute_length, 2))  # => Output: 18.81 -- the PROVABLY shortest possible tour
print(  # => opens the greedy-tour-length print call
    round(nn_length, 2)  # => greedy's own tour length, rounded for display
)  # => Output: 22.19 -- greedy's tour, longer but found MUCH faster

assert brute_length <= nn_length  # => brute force NEVER loses -- it tries every option
assert (  # => opens the greedy-is-meaningfully-worse check
    nn_length
    > brute_length
    * 1.1  # => greedy's tour is at least 10% longer, genuinely suboptimal
)  # => confirms the heuristic is genuinely SUBOPTIMAL here
assert (  # => opens the exact-search-space-size check
    math.factorial(len(cities) - 1)
    == 720  # => 6! = 720, the exact brute-force search space
)  # => brute force's search space: 6! orderings for 7 cities
print("ex-75 OK")  # => Output: ex-75 OK
