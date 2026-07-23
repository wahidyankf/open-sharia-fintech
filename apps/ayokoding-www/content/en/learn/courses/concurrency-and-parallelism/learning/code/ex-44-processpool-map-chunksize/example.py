"""Example 44: `ProcessPoolExecutor.map` With a `chunksize` -- Same Result, Less IPC Overhead."""

from concurrent.futures import ProcessPoolExecutor  # => co-24: multiple OS processes, each its own GIL

DATA = list(range(2000))  # => DATA: a modest-sized workload -- enough to make chunking meaningful


def square(n: int) -> int:  # => a top-level function -- REQUIRED, so child processes can pickle+import it
    return n * n  # => trivial CPU work; the point here is chunksize's effect on IPC, not the math


if __name__ == "__main__":  # => module entry point
    with ProcessPoolExecutor(max_workers=4) as pool_default:  # => 4 worker processes, default chunksize
        default_result = list(pool_default.map(square, DATA))  # => chunksize=1 by default: one IPC round-trip PER item
    print(f"default_result[:5]={default_result[:5]}")  # => Output: default_result[:5]=[0, 1, 4, 9, 16]

    with ProcessPoolExecutor(max_workers=4) as pool_chunked:  # => a FRESH pool -- same worker count
        chunked_result = list(pool_chunked.map(square, DATA, chunksize=100))  # => 100 items per IPC round-trip
    print(f"chunked_result[:5]={chunked_result[:5]}")  # => Output: chunked_result[:5]=[0, 1, 4, 9, 16]

    expected = [square(n) for n in DATA]  # => expected: the serial, single-process baseline -- ground truth

    # => `chunksize` only changes HOW MANY items are batched into each inter-process message before a
    # => worker processes them -- it does NOT change the RESULT. A larger chunksize amortizes the fixed
    # => per-message pickling/IPC cost across more items, which usually helps throughput on many small
    # => tasks; too large a chunksize can hurt load balancing across workers. Either way, `.map()`
    # => ALWAYS returns results in the SAME order as the input iterable, regardless of chunksize or which
    # => worker process happened to finish first -- unlike `as_completed` (ex-42), order here is preserved.
    assert default_result == expected  # => confirms chunksize=1 (the default) gives the correct aggregate
    assert chunked_result == expected  # => confirms chunksize=100 gives the IDENTICAL correct aggregate
    assert default_result == chunked_result  # => confirms chunksize affects performance, never correctness
    print("ex-44 OK")  # => Output: ex-44 OK
