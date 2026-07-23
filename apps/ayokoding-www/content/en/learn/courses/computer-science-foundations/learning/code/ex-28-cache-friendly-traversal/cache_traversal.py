# learning/code/ex-28-cache-friendly-traversal/cache_traversal.py
"""Example 28: Row-Major vs. Column-Major Traversal of a 2-D Array."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import array  # => co-16: array.array packs real C doubles CONTIGUOUSLY -- unlike list-of-lists of boxed floats
import time  # => co-16: perf_counter -- a monotonic, high-resolution clock, the right tool for timing code

N = 1400  # => co-16: N*N doubles (~15.7 MB) -- large enough to exceed typical L2 cache, small enough to run fast
TRIALS = 3  # => co-16: best-of-3 -- reduces noise from other processes briefly stealing the CPU


def build_matrix(n: int) -> array.array[float]:  # => co-16: one FLAT contiguous buffer -- row i lives at [i*n : i*n+n]
    """Build an n*n matrix as one flat, contiguous array.array of doubles (row-major layout)."""  # => co-16: documents build_matrix's contract -- no runtime output, just sets its __doc__
    flat = array.array("d", [0.0]) * (n * n)  # => co-16: n*n contiguous 8-byte slots, all zero-initialized
    for k in range(n * n):  # => co-16: fill with distinguishable, cheap-to-compute values
        flat[k] = float(k % 97)  # => co-16: content is irrelevant to the timing -- only the ACCESS PATTERN matters
    return flat  # => co-16: returns this computed value to the caller


def row_major_sum(flat: array.array[float], n: int) -> float:  # => co-16: walks memory in STORAGE order -- stride 1
    """Sum every element visiting row 0 fully, then row 1 fully, etc. -- matches the storage layout."""  # => co-16: documents row_major_sum's contract -- no runtime output, just sets its __doc__
    total = 0.0  # => co-16: accumulator -- the returned value only proves correctness, not speed
    for i in range(n):  # => co-16: outer loop over rows
        base = i * n  # => co-16: row i's starting flat index -- computed once per row, not once per element
        for j in range(n):  # => co-16: inner loop walks CONSECUTIVE flat indices -- sequential memory access
            total += flat[base + j]  # => co-16: stride-1 access -- exactly how the CPU's cache line prefetcher likes it
    return total  # => co-16: returns this computed value to the caller


def col_major_sum(flat: array.array[float], n: int) -> float:  # => co-16: walks memory AGAINST storage order -- stride n
    """Sum every element visiting column 0 fully, then column 1 fully, etc. -- fights the storage layout."""  # => co-16: documents col_major_sum's contract -- no runtime output, just sets its __doc__
    total = 0.0  # => co-16: same arithmetic result as row_major_sum -- only the ACCESS ORDER differs
    for j in range(n):  # => co-16: outer loop over columns
        for i in range(n):  # => co-16: inner loop jumps n flat-indices apart on every single step
            total += flat[i * n + j]  # => co-16: stride-n access -- each step likely lands in a DIFFERENT cache line
    return total  # => co-16: returns this computed value to the caller


if __name__ == "__main__":  # => co-16: entry point -- this block runs only when the file executes directly, not on import
    matrix = build_matrix(N)  # => co-16: one shared buffer -- both traversal orders read the SAME data
    row_times: list[float] = []  # => co-16: one measured duration per trial, row-major
    col_times: list[float] = []  # => co-16: one measured duration per trial, column-major
    for _ in range(TRIALS):  # => co-16: repeat both traversals, keeping the BEST (least-noisy) time of each
        t0 = time.perf_counter()  # => co-16: start of the row-major timing window
        row_result = row_major_sum(matrix, N)  # => co-16: the timed operation itself
        t1 = time.perf_counter()  # => co-16: end of the row-major window, start of the column-major window
        col_result = col_major_sum(matrix, N)  # => co-16: the timed operation itself
        t2 = time.perf_counter()  # => co-16: end of the column-major window
        row_times.append(t1 - t0)  # => co-16: this trial's row-major duration
        col_times.append(t2 - t1)  # => co-16: this trial's column-major duration
        assert row_result == col_result, "both traversal orders must sum to the identical total"  # => co-16
    best_row = min(row_times)  # => co-16: best-of-3 -- the closest approximation to each method's true cost
    best_col = min(col_times)  # => co-16: same best-of-3 policy applied to the column-major trials
    print(f"row-major best of {TRIALS}: {best_row:.4f}s")  # => co-16: prints the row-major measurement
    print(f"col-major best of {TRIALS}: {best_col:.4f}s")  # => co-16: prints the column-major measurement
    print(f"col-major / row-major ratio: {best_col / best_row:.2f}x")  # => co-16: how much slower column-major was
    assert best_row < best_col, "row-major (sequential access) must be measurably faster than column-major"  # => co-16
    print(f"Row-major is measurably faster: True")  # => co-16: reached only if the timing assert above held
    # => co-16: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
