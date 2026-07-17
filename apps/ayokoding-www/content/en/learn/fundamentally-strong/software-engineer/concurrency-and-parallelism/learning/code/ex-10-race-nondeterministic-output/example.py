"""Example 10: A Race's Output Is Nondeterministic Across Runs."""

import random  # => the source of run-to-run variability this example measures
import threading  # => two threads racing on one shared counter, as in ex-08
import time  # => `time.sleep(0)` occasionally widens the race window

ITERATIONS_PER_THREAD = 500  # => small and fast -- run several times to observe VARIATION, not one bug


def racy_increment(counter: list[int]) -> None:  # => the SAME lost-update shape as ex-08
    for _ in range(ITERATIONS_PER_THREAD):  # => runs the racy increment this many times
        value = counter[0]  # => READ the shared counter into a local
        if random.random() < 0.5:  # => a COIN FLIP -- sometimes yields, sometimes doesn't
            time.sleep(0)  # => yields the GIL only on the "heads" branch -- the source of variation
        counter[0] = value + 1  # => WRITE BACK the (possibly stale) local value + 1


def one_race() -> int:  # => runs the two-thread race ONCE, returns the final total
    counter = [0]  # => a fresh counter for this single run
    threads = [threading.Thread(target=racy_increment, args=(counter,)) for _ in range(2)]
    for t in threads:  # => launches both threads
        t.start()  # => the coin flip inside racy_increment makes EVERY run's interleaving different
    for t in threads:  # => waits for both to finish
        t.join()  # => join() blocks until that thread's racy_increment() call returns
    return counter[0]  # => this run's final total -- expected to differ from OTHER runs' totals


if __name__ == "__main__":  # => module entry point
    totals = [one_race() for _ in range(5)]  # => totals: the final count from 5 INDEPENDENT races
    print(totals)  # => Output: [something, something-else, ...] -- rarely, if ever, all identical

    distinct = set(totals)  # => distinct: the set of unique totals observed across the 5 runs
    expected = 2 * ITERATIONS_PER_THREAD  # => expected: the correct total if the race never lost updates
    print(f"distinct_count={len(distinct)} expected={expected}")  # => Output: distinct_count=... expected=1000

    # => Because each run's coin flips land differently, the exact number of lost updates
    # => varies from run to run -- this is co-08's core claim: a race condition's RESULT depends
    # => on the nondeterministic interleaving of operations, not on the code itself.
    assert len(distinct) > 1  # => confirms the 5 runs did NOT all produce the identical total
    assert all(t <= expected for t in totals)  # => confirms no run ever exceeded the correct total
    print("ex-10 OK")  # => Output: ex-10 OK
