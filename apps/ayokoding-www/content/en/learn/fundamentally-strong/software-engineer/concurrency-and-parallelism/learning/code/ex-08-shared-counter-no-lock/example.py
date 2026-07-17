"""Example 8: A Shared Counter Without a Lock Loses Updates."""

import threading  # => two threads racing on one shared variable
import time  # => `time.sleep(0)` forces a context-switch window between read and write

ITERATIONS_PER_THREAD = 2_000  # => small but reliable: each iteration deliberately widens the race window


def increment_many(counter: list[int]) -> None:  # => counter[0] is the shared mutable state
    for _ in range(ITERATIONS_PER_THREAD):  # => runs the unsynchronized increment this many times
        value = counter[0]  # => READ counter[0] into a LOCAL variable -- step 1 of 3
        time.sleep(0)  # => yields the GIL RIGHT HERE -- widens the window for co-08's lost update
        counter[0] = value + 1  # => WRITE BACK the stale local `value` + 1 -- step 3, using OLD data


def racing_total() -> int:  # => runs two threads incrementing the SAME counter, no lock
    counter = [0]  # => a one-element list stands in for a shared mutable int (ints are immutable)
    threads = [threading.Thread(target=increment_many, args=(counter,)) for _ in range(2)]
    # => two threads, both targeting the SAME counter list -- a classic shared-mutable-state hazard
    for t in threads:  # => launches both racing threads
        t.start()  # => both now interleave reads/writes to counter[0] with no coordination
    for t in threads:  # => waits for both to finish
        t.join()  # => join() blocks until that thread's increment_many() call returns
    return counter[0]  # => the FINAL value -- expected to be wrong due to lost updates


if __name__ == "__main__":  # => module entry point
    expected = 2 * ITERATIONS_PER_THREAD  # => expected: what the total WOULD be if increments never raced
    actual = racing_total()  # => actual: what the total ACTUALLY is after the unsynchronized race
    print(f"expected={expected} actual={actual}")  # => Output: expected=4000 actual=2000 (roughly)

    # => Between `value = counter[0]` and `counter[0] = value + 1`, the OTHER thread reads the SAME
    # => stale `counter[0]`, and whichever thread writes last silently overwrites the other's
    # => increment -- a LOST UPDATE, the defining symptom of co-07's shared-mutable-state hazard.
    assert actual < expected  # => confirms at least one increment was lost to the unsynchronized race
    print("ex-08 OK")  # => Output: ex-08 OK
