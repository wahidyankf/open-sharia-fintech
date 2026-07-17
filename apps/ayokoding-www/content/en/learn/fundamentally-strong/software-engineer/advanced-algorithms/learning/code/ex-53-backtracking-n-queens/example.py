"""Example 53: N-Queens by Backtracking with Pruning."""

# Backtracking (co-25) places queens column by column, checking safety
# against every PREVIOUSLY placed queen; the moment a placement is unsafe,
# it prunes -- never even exploring the rest of that doomed branch further.


def solve_n_queens(n: int) -> int:  # => returns the COUNT of distinct solutions
    solutions = [0]  # => a one-element list used as a mutable counter in the closure
    columns_used: set[int] = set()  # => which columns already have a queen
    diag1_used: set[int] = set()  # => which "row - col" diagonals already have a queen
    diag2_used: set[int] = set()  # => which "row + col" diagonals already have a queen

    def place(row: int) -> None:  # => tries placing a queen in every column of this row
        if row == n:  # => base case: every row has a safely placed queen
            solutions[0] += 1  # => one more complete, valid solution found
            return  # => backtracks to try other placements at the previous row
        for col in range(n):  # => tries every column in this row
            if (
                col in columns_used
                or (row - col) in diag1_used
                or (row + col) in diag2_used
            ):  # => THE PRUNE: this column is attacked by an earlier queen
                continue  # => skip this column entirely -- never explore it further
            columns_used.add(col)  # => marks this column as occupied
            diag1_used.add(row - col)  # => marks this "/" diagonal as occupied
            diag2_used.add(row + col)  # => marks this "\" diagonal as occupied
            place(row + 1)  # => recurses to place the NEXT row's queen
            columns_used.remove(col)  # => THE BACKTRACK: undoes this choice
            diag1_used.remove(row - col)  # => frees this diagonal for other branches
            diag2_used.remove(row + col)  # => frees this diagonal too

    place(0)  # => starts placing from row 0
    return solutions[0]  # => the total count of valid N-queens solutions


known_counts: dict[int, int] = {  # => OEIS A000170: the known solution count per N
    4: 2,
    5: 10,
    6: 4,
    7: 40,
    8: 92,
}
for (
    n,
    expected,
) in known_counts.items():  # => verifies N=4..8, as the syllabus specifies
    found = solve_n_queens(n)  # => backtracking's own count
    print(f"N={n}: {found}")  # => Output: one "N=n: count" line per N
    assert found == expected  # => confirms against the well-known OEIS counts
print("ex-53 OK")  # => Output: ex-53 OK
