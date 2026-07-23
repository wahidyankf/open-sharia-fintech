"""Kata 9 (before): backtracking never un-marks a placed queen, so a rejected branch poisons every later attempt."""


def count_solutions(n: int) -> int:
    cols: set[int] = set()
    solutions = 0

    def is_safe(row: int, col: int, placed: list[int]) -> bool:
        for r, c in enumerate(placed):
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def place(row: int, placed: list[int]) -> None:
        nonlocal solutions
        if row == n:
            solutions += 1
            return
        for col in range(n):
            if col in cols:
                continue
            if is_safe(row, col, placed):
                cols.add(col)
                placed.append(col)
                place(row + 1, placed)
                # BUG: never removes `col` from `cols` or pops `placed` -- the board is never truly reset

    place(0, [])
    return solutions


print(count_solutions(4))
print(
    count_solutions(4) == 2
)  # N=4 has exactly 2 valid solutions -- the true, well-known answer
