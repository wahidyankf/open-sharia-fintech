"""Example 56: pytest verification for Grid Word Search."""

from example import word_search


def test_finds_a_word_that_exists_along_a_valid_path() -> None:
    grid = [["A", "B"], ["C", "D"]]
    assert word_search(grid, "ABDC") is True  # => A -> B -> D -> C, all adjacent


def test_rejects_a_word_requiring_cell_reuse() -> None:
    grid = [["A", "A"]]
    assert word_search(grid, "AAA") is False  # => only 2 cells, word needs 3 A's


def test_single_cell_grid_matches_single_character_word() -> None:
    grid = [["X"]]
    assert word_search(grid, "X") is True
    assert word_search(grid, "Y") is False


# => Run: pytest -- Output: 3 passed
