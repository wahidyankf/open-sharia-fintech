"""Example 39: pytest verification for Constraint Mini Sudoku (4x4)."""

from example import box_id, solve


def test_solved_board_has_valid_rows_columns_and_boxes() -> None:
    puzzle = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]  # => same puzzle as the demo
    solution = solve([row[:] for row in puzzle])  # => solve a defensive copy
    assert solution is not None  # => this puzzle is solvable
    for row in solution:  # => row constraint
        assert sorted(row) == [1, 2, 3, 4]
    for col in range(4):  # => column constraint
        assert sorted(solution[r][col] for r in range(4)) == [1, 2, 3, 4]
    boxes: dict[tuple[int, int], list[int]] = {}  # => box constraint
    for r in range(4):
        for c in range(4):
            boxes.setdefault(box_id(r, c), []).append(solution[r][c])
    for values in boxes.values():
        assert sorted(values) == [1, 2, 3, 4]


def test_original_puzzle_is_not_mutated_by_solving_a_copy() -> None:
    puzzle = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]  # => fresh puzzle for this test
    before = [row[:] for row in puzzle]  # => snapshot before solving
    solve([row[:] for row in puzzle])  # => solve a copy, discard the result
    assert puzzle == before  # => the original puzzle list is byte-identical to its snapshot


# => Run: pytest -- Output: 2 passed
