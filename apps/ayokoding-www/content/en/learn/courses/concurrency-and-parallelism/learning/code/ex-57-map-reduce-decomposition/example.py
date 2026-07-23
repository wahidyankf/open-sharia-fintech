"""Example 57: Map-Reduce -- Split the Work, Combine the Partial Results."""

from concurrent.futures import ProcessPoolExecutor  # => co-24: genuine parallel workers for the "map" phase

DATA = list(range(1, 100_001))  # => DATA: the full dataset to sum -- 100,000 integers
CHUNK_COUNT = 4  # => how many pieces to split DATA into for the "map" phase


def chunk_list(data: list[int], chunks: int) -> list[list[int]]:  # => splits `data` into `chunks` near-equal pieces
    size = len(data) // chunks + 1  # => size: the max length of each chunk (rounds up to cover any remainder)
    return [data[i : i + size] for i in range(0, len(data), size)]  # => a list of `chunks` sub-lists, covering ALL of `data`


def partial_sum(chunk: list[int]) -> int:  # => the "map" step -- a top-level function, so it can be pickled to a worker
    return sum(chunk)  # => reduces ONE chunk down to a single partial total


def map_reduce_sum(data: list[int], chunks: int) -> int:
    pieces = chunk_list(data, chunks)  # => pieces: `data` split into `chunks` independent sub-lists ("map" input)
    with ProcessPoolExecutor(max_workers=chunks) as pool:  # => one worker process per chunk (co-24)
        partial_sums = list(pool.map(partial_sum, pieces))  # => the "map" phase -- each chunk summed IN PARALLEL
    return sum(partial_sums)  # => the "reduce" phase -- combines every partial total into the final answer


if __name__ == "__main__":  # => module entry point
    serial_total = sum(DATA)  # => serial_total: the single-process ground truth, computed the "boring" way
    map_reduce_total = map_reduce_sum(DATA, CHUNK_COUNT)  # => map_reduce_total: computed via the split-then-combine pattern
    print(f"serial_total={serial_total} map_reduce_total={map_reduce_total}")
    # => Output: serial_total=5000050000 map_reduce_total=5000050000

    # => Map-reduce decomposes a large computation into two phases: MAP (apply an independent function to
    # => each piece of the input, in parallel -- here, summing one chunk) and REDUCE (combine every
    # => piece's partial result into the final answer -- here, summing the partial sums). Because SUM is
    # => associative, splitting it this way is provably correct: the combined result is IDENTICAL to
    # => summing the whole dataset serially, while the map phase itself can exploit multiple processes
    # => (co-24) -- the same decomposition principle behind Amdahl's-law reasoning in ex-56 (co-28).
    assert map_reduce_total == serial_total  # => confirms the parallel decomposition matches the serial baseline EXACTLY
    print("ex-57 OK")  # => Output: ex-57 OK
