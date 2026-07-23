"""Example 38: pytest verification for Constraint Map Coloring."""

from example import solve_coloring


def test_no_adjacent_regions_share_a_color() -> None:
    adjacency = {"west": ["central"], "central": ["west", "east"], "east": ["central"]}
    colors = ["red", "green", "blue"]
    result = solve_coloring(adjacency, colors)
    assert result is not None  # => a valid 3-coloring must exist for this simple adjacency graph
    for region, neighbors in adjacency.items():  # => check every declared constraint holds
        for neighbor in neighbors:
            assert result[region] != result[neighbor]  # => the core map-coloring constraint


def test_two_colors_are_insufficient_for_a_triangle() -> None:
    triangle = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}  # => every region touches both others
    assert solve_coloring(triangle, ["red", "green"]) is None  # => a triangle needs at least 3 colors


# => Run: pytest -- Output: 2 passed
