"""Example 7: Starting Many Threads and Joining Them All."""  # => co-06: the start-many-then-join-many pattern

import threading  # => builds on ex-06 with N threads instead of one

COUNT = 8  # => how many worker threads this example spawns


def worker(worker_id: int, results: list[int]) -> None:  # => each thread runs with its OWN id
    results.append(worker_id)  # => appends this worker's id -- list.append is thread-safe in CPython


def run_all(count: int) -> list[int]:  # => spawns `count` threads, joins every one, returns results
    results: list[int] = []  # => shared list every worker appends its id into
    threads = [threading.Thread(target=worker, args=(i, results)) for i in range(count)]
    # => builds `count` Thread objects, each closing over its own `i` via args=
    for t in threads:  # => a FIRST loop that launches every thread
        t.start()  # => start() -- all `count` threads may now be running concurrently
    for t in threads:  # => a SECOND, separate loop that waits for every thread
        t.join()  # => join() blocks until THIS thread finishes -- iterating collects them all
    return results  # => results now holds exactly `count` ids, order not guaranteed


if __name__ == "__main__":  # => module entry point
    ids = run_all(COUNT)  # => ids: every worker's id, in whatever order threads actually finished
    print(sorted(ids))  # => Output: [0, 1, 2, 3, 4, 5, 6, 7]

    # => two separate loops matter: starting-then-joining-in-the-same-loop would serialize them.
    assert len(ids) == COUNT  # => confirms every single thread ran exactly once (none dropped)
    assert sorted(ids) == list(range(COUNT))  # => confirms every id 0..7 appeared, no duplicates
    print("ex-07 OK")  # => Output: ex-07 OK
