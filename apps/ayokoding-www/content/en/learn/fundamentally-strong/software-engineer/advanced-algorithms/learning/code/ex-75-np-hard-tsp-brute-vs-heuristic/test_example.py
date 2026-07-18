"""Example 75: pytest verification for TSP Brute Force vs Nearest-Neighbor."""

from example import Point, brute_force_tsp, nearest_neighbor_tsp, tour_length


def test_brute_force_finds_the_optimal_square_tour() -> None:
    # => four corners of a unit square: the optimal tour just walks the perimeter
    square: list[Point] = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
    order, length = brute_force_tsp(square)
    assert round(length, 4) == 4.0  # => perimeter of a unit square: 1+1+1+1
    assert len(order) == 4 and set(order) == {0, 1, 2, 3}


def test_nearest_neighbor_always_visits_every_city_exactly_once() -> None:
    cities: list[Point] = [(0.0, 0.0), (5.0, 0.0), (5.0, 5.0), (0.0, 5.0), (2.5, 2.5)]
    order, _length = nearest_neighbor_tsp(cities)
    assert sorted(order) == list(
        range(len(cities))
    )  # => a valid permutation, no repeats


def test_brute_force_never_beats_its_own_reported_length() -> None:
    triangle: list[Point] = [(0.0, 0.0), (3.0, 0.0), (0.0, 4.0)]
    order, length = brute_force_tsp(triangle)
    assert (
        tour_length(order, triangle) == length
    )  # => the reported length matches recomputation


# => Run: pytest -- Output: 3 passed
