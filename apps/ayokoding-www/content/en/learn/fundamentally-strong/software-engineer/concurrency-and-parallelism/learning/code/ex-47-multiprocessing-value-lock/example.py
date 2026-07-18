"""Example 47: A Shared `multiprocessing.Value`, Protected by ITS OWN Built-In Lock."""

import multiprocessing  # => co-24: true parallel processes; co-11: still need a lock for shared state
from multiprocessing.sharedctypes import Synchronized  # => Synchronized: the type `Value(...)` actually returns

INCREMENTS_PER_PROCESS = 5000  # => how many times each of the 4 processes increments the shared total
PROCESS_COUNT = 4  # => four independent OS processes, all incrementing the SAME shared counter


def increment_many(shared_total: "Synchronized[int]", times: int) -> None:  # => runs in a SEPARATE process
    for _ in range(times):  # => repeats the increment `times` times, once per call
        with shared_total.get_lock():  # => acquires the Value's OWN built-in lock (a real, cross-process lock)
            shared_total.value += 1  # => the ENTIRE read-modify-write happens while holding that lock


if __name__ == "__main__":  # => module entry point -- required for multiprocessing's `spawn` start method
    shared_total = multiprocessing.Value("i", 0)  # => "i": a C `int`, backed by shared memory ACROSS processes
    processes = [
        multiprocessing.Process(target=increment_many, args=(shared_total, INCREMENTS_PER_PROCESS))
        for _ in range(PROCESS_COUNT)  # => builds PROCESS_COUNT independent Process objects, not yet started
    ]  # => processes: exactly PROCESS_COUNT Process objects, all sharing the SAME `shared_total`

    for p in processes:  # => starts every process
        p.start()  # => each process begins incrementing shared_total.value, protected by its own lock
    for p in processes:  # => waits for every process to finish its increments
        p.join()  # => join() blocks until that process has fully exited

    expected = PROCESS_COUNT * INCREMENTS_PER_PROCESS  # => expected: the mathematically correct total
    print(f"expected={expected} actual={shared_total.value}")  # => Output: expected=20000 actual=20000

    # => `multiprocessing.Value` allocates its data in SHARED MEMORY, visible to every process that holds
    # => a reference to it -- unlike a plain Python object, which each process would get its own COPY of
    # => (ex-45). By default it also comes with its OWN `RLock`, retrievable via `get_lock()`, which is a
    # => genuine CROSS-PROCESS lock (unlike `threading.Lock`, which only coordinates threads within ONE
    # => process). Without holding that lock around the read-modify-write, `+= 1` would lose updates
    # => across processes exactly like ex-08's threads did -- shared memory alone does not imply safety.
    assert shared_total.value == expected  # => confirms no increment was lost across any of the 4 processes
    print("ex-47 OK")  # => Output: ex-47 OK
