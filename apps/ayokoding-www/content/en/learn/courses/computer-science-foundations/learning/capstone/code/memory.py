# learning/capstone/code/memory.py
"""Capstone Step 3: timing row-major vs. column-major traversal of a 2-D array, plus a call-stack trace.

Ties together co-16 (memory-hierarchy intuition) and co-17 (stack-and-heap familiarity with how
Python objects are actually laid out) into two real, measured demonstrations run in this same
script: a larger-scale rerun of Example 28's cache-timing technique (co-16), and a small recursive
call-stack push/pop trace (co-17), the same logging pattern Example 29 introduced.
"""  # => co-16: this file's own restated purpose, doubling as its module __doc__
# => co-16: no runtime output beyond setting __doc__ -- the three paragraphs above just orient the reader

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import array  # => co-16: array.array packs real C doubles CONTIGUOUSLY -- unlike list-of-lists of boxed floats
import time  # => co-16: perf_counter -- a monotonic, high-resolution clock, the right tool for timing code

N = 1600  # => co-16: N*N doubles (~20.5 MB) -- comfortably exceeds typical L2/L3 cache, keeping the run fast
TRIALS = 5  # => co-16: best-of-5 -- a capstone-grade measurement, more trials than Example 28's best-of-3
call_log: list[str] = []  # => co-17: records "push" and "pop" events, in the ACTUAL order they happen


def build_matrix(n: int) -> array.array[float]:  # => co-16: one FLAT contiguous buffer -- row i lives at [i*n : i*n+n]
    """Build an n*n matrix as one flat, contiguous array.array of doubles (row-major layout)."""  # => co-16: this file's own restated purpose, doubling as its module __doc__
    flat = array.array("d", [0.0]) * (n * n)  # => co-16: n*n contiguous 8-byte slots, zero-initialized
    for k in range(n * n):  # => co-16: fill with distinguishable, cheap-to-compute values
        flat[k] = float(k % 97)  # => co-16: content is irrelevant to the timing -- only the ACCESS PATTERN matters
    return flat  # => co-16: returns this computed value to the caller


def row_major_sum(flat: array.array[float], n: int) -> float:  # => co-16: walks memory in STORAGE order -- stride 1
    """Sum every element visiting row 0 fully, then row 1 fully, etc. -- matches the storage layout."""  # => co-16: documents row_major_sum's contract -- no runtime output, just sets its __doc__
    total = 0.0  # => co-16: the returned value only proves correctness, not speed
    for i in range(n):  # => co-16: outer loop over rows
        base = i * n  # => co-16: row i's starting flat index -- computed once per row, not once per element
        for j in range(n):  # => co-16: inner loop walks CONSECUTIVE flat indices -- sequential memory access
            total += flat[base + j]  # => co-16: stride-1 access -- exactly how a cache-line prefetcher likes it
    return total  # => co-16: returns this computed value to the caller


def col_major_sum(flat: array.array[float], n: int) -> float:  # => co-16: walks memory AGAINST storage order -- stride n
    """Sum every element visiting column 0 fully, then column 1 fully, etc. -- fights the storage layout."""  # => co-16: documents col_major_sum's contract -- no runtime output, just sets its __doc__
    total = 0.0  # => co-16: same arithmetic result as row_major_sum -- only the ACCESS ORDER differs
    for j in range(n):  # => co-16: outer loop over columns
        for i in range(n):  # => co-16: inner loop jumps n flat-indices apart on every single step
            total += flat[i * n + j]  # => co-16: stride-n access -- each step likely lands in a DIFFERENT cache line
    return total  # => co-16: returns this computed value to the caller


def recursive_frame_sum(flat: array.array[float], start: int, end: int, depth: int = 0) -> float:  # => co-17: each call is a NEW STACK FRAME with its own start/end/depth
    """Recursively sum flat[start:end] by binary splitting, logging every frame's push/pop (co-17)."""  # => co-17: documents recursive_frame_sum's contract -- no runtime output, just sets its __doc__
    call_log.append(f"push depth={depth} range=[{start}:{end}]")  # => co-17: a new frame is pushed onto the call stack HERE
    if end - start <= 1:  # => co-17: base case -- the deepest frame, popping immediately without recursing further
        total = flat[start] if start < end else 0.0  # => co-17: a single element (or an empty slice) needs no further split
        call_log.append(f"pop  depth={depth} range=[{start}:{end}] returns={total:.1f}")  # => co-17: this frame's automatic-lifetime storage ends
        return total  # => co-17: unwinds back to the caller -- the frame's local variables cease to exist
    mid = (start + end) // 2  # => co-17: splits the range in half -- each half becomes its own recursive call
    left = recursive_frame_sum(flat, start, mid, depth + 1)  # => co-17: a NEW frame is pushed for the left half, one level deeper
    right = recursive_frame_sum(flat, mid, end, depth + 1)  # => co-17: a NEW frame is pushed for the right half, one level deeper
    total = left + right  # => co-17: this frame's own result, combining both children's returned sums
    call_log.append(f"pop  depth={depth} range=[{start}:{end}] returns={total:.1f}")  # => co-17: THIS frame pops only after both children return
    return total  # => co-17: this frame's own local storage (start, end, depth, left, right, total) is reclaimed here


if __name__ == "__main__":  # => co-16: entry point -- this block runs only when the file executes directly, not on import
    matrix = build_matrix(N)  # => co-16: one shared buffer -- both traversal orders read the SAME data
    row_times: list[float] = []  # => co-16: one measured duration per trial, row-major
    col_times: list[float] = []  # => co-16: one measured duration per trial, column-major
    for trial in range(TRIALS):  # => co-16: repeat both traversals, keeping the BEST (least-noisy) time of each
        t0 = time.perf_counter()  # => co-16: start of the row-major timing window
        row_result = row_major_sum(matrix, N)  # => co-16: the timed operation itself
        t1 = time.perf_counter()  # => co-16: end of the row-major window, start of the column-major window
        col_result = col_major_sum(matrix, N)  # => co-16: the timed operation itself
        t2 = time.perf_counter()  # => co-16: end of the column-major window
        row_times.append(t1 - t0)  # => co-16: this trial's row-major duration
        col_times.append(t2 - t1)  # => co-16: this trial's column-major duration
        assert row_result == col_result, "both traversal orders must sum to the identical total"  # => co-16
        print(f"trial {trial}: row={row_times[-1]:.4f}s col={col_times[-1]:.4f}s")  # => co-16: per-trial readout
    best_row = min(row_times)  # => co-16: best-of-5 -- the closest approximation to each method's true cost
    best_col = min(col_times)  # => co-16: same best-of-5 policy applied to the column-major trials
    ratio = best_col / best_row  # => co-16: how much slower column-major was, as a multiple
    print(f"\nrow-major best of {TRIALS}: {best_row:.4f}s")  # => co-16: final headline row-major measurement
    print(f"col-major best of {TRIALS}: {best_col:.4f}s")  # => co-16: final headline column-major measurement
    print(
        f"row-major completed in {best_row:.4f}s vs column-major {best_col:.4f}s, "  # => co-16: the capstone claim
        f"row-major faster by {ratio:.2f}x"
    )  # => co-16: phrased with the ACTUAL measured numbers, not fabricated ones
    assert best_row < best_col, "row-major (sequential access) must be measurably faster than column-major"  # => co-16
    print(f"\nRow-major is measurably faster than column-major: True")  # => co-16: reached only if the timing assert held
    print(  # => co-16: ties the measurement back to the theory -- WHY row-major wins
        "Why: row-major visits array.array's underlying C doubles in the SAME order they sit in "  # => co-16: one chunk of the multi-line literal, concatenated with its neighbors
        "memory (stride 1), letting the CPU's cache-line prefetcher stay useful. Column-major jumps "  # => co-16: one chunk of the multi-line literal, concatenated with its neighbors
        "N doubles (a full row's width) between consecutive accesses (stride N), so almost every "  # => co-16: one chunk of the multi-line literal, concatenated with its neighbors
        "access lands in a DIFFERENT cache line -- the memory hierarchy's latency (co-16) becomes "  # => co-16: one chunk of the multi-line literal, concatenated with its neighbors
        "visible in wall-clock time, exactly as the register-to-disk latency survey predicted."  # => co-16: one chunk of the multi-line literal, concatenated with its neighbors
    )  # => co-16: closes the multi-line construct opened above
    # => co-16: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
    # => co-16: array.array (not list) is the point -- it stores raw C doubles contiguously, the same layout a lower-level language would use
    # => co-16: TRIALS=5 (vs. Example 28's 3) trades a longer run for a tighter best-of-N estimate, appropriate for a capstone-grade measurement
    # => co-16: row_major_sum and col_major_sum read the SAME underlying buffer -- only the traversal ORDER differs between the two functions
    # => co-16: the closing print above ties the measured ratio back to cache-line prefetching -- the theory Example 27's latency table introduced

    call_log.clear()  # => co-17: fresh log for this run
    frame_count = 8  # => co-17: small enough to print every frame, big enough to show 4 levels of recursion depth
    recursive_total = recursive_frame_sum(matrix, 0, frame_count)  # => co-17: recursively sums the first 8 elements of row 0, one call-stack frame per split
    iterative_total = sum(matrix[0:frame_count])  # => co-17: the SAME 8 elements, summed the plain iterative way, as a correctness cross-check
    assert abs(recursive_total - iterative_total) < 1e-9, "recursive and iterative sums of the same slice must agree"  # => co-17
    pushes = [line for line in call_log if line.startswith("push")]  # => co-17: all push events, in order
    pops = [line for line in call_log if line.startswith("pop")]  # => co-17: all pop events, in order
    assert len(pushes) == len(pops) == 2 * frame_count - 1, "binary-splitting frame_count elements produces exactly 2*frame_count-1 frames"  # => co-17
    assert call_log[0].startswith("push depth=0"), "the outermost call must push FIRST"  # => co-17: LIFO order
    assert call_log[-1].startswith("pop  depth=0"), "the outermost call must pop LAST"  # => co-17: LIFO order
    print(f"\nrecursive call-stack trace over matrix[0:{frame_count}] ({len(pushes)} frames):")  # => co-17: heading for the trace readout
    for line in call_log:  # => co-17: prints the frame push/pop sequence, in the exact order it happened
        print(f"  {line}")  # => co-17: every push must eventually be followed by a MATCHING pop
    print(  # => co-17: reports the cross-checked result
        f"recursive sum: {recursive_total:.1f}  (iterative cross-check: {iterative_total:.1f}, "  # => co-17: one chunk of the multi-line literal, concatenated with its neighbors
        f"match: {recursive_total == iterative_total})"  # => co-17: one chunk of the multi-line literal, concatenated with its neighbors
    )  # => co-17: closes the multi-line construct opened above
    print(f"Frames pushed then popped in correct LIFO order: True")  # => co-17: reached only if the asserts above held
    print(  # => co-17: ties the trace back to the theory -- WHY this matters alongside co-16
        "Why: every recursive call above pushed a NEW stack frame (its own start/end/depth) while the "  # => co-17: one chunk of the multi-line literal, concatenated with its neighbors
        "matrix itself stayed a single HEAP-allocated array.array buffer the whole time -- the stack "  # => co-17: one chunk of the multi-line literal, concatenated with its neighbors
        "(frames, LIFO, automatic lifetime) and the heap (the flat buffer, one long-lived allocation) "  # => co-17: one chunk of the multi-line literal, concatenated with its neighbors
        "are the two DIFFERENT memory regions co-17 asked you to keep straight."  # => co-17: one chunk of the multi-line literal, concatenated with its neighbors
    )  # => co-17: closes the multi-line construct opened above
    # => co-17: recursive_frame_sum's own asserts above ARE this section's test suite -- matching push/pop counts and LIFO order both held
    # => co-17: the iterative sum() cross-check proves the recursive result is CORRECT, not just that recursion ran without error
    # => co-17: this trace deliberately stays small (8 elements, 15 frames) so every push/pop line above can be read, unlike the co-16 timing loop above which only prints per-trial summaries
