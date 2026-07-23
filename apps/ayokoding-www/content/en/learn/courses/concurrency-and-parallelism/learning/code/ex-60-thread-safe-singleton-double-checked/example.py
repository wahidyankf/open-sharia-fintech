"""Example 60: Double-Checked Locking -- A Lazily-Built Singleton, Safe Under Contention."""

import threading  # => co-11: a lock guards the ONE moment construction actually happens
import time  # => `sleep(0)` widens the race window, proven reliable since ex-08

_lock = threading.Lock()  # => _lock: the module-level lock guarding the SLOW path (construction) only
_instance: "ExpensiveResource | None" = None  # => _instance: None until the FIRST successful construction
construction_count = [0]  # => construction_count: how many times the expensive constructor actually ran


class ExpensiveResource:  # => stands in for something costly to build -- a config object, a connection pool
    def __init__(self) -> None:
        time.sleep(0)  # => widens the window between the checks below and this constructor actually running
        construction_count[0] += 1  # => records EVERY construction attempt that reaches this line


def get_instance() -> ExpensiveResource:  # => the double-checked-locking accessor every thread calls
    global _instance  # => reassigns the MODULE-level singleton, not a local shadow
    if _instance is None:  # => CHECK 1 (unlocked, fast path): usually True only on the very FIRST few calls
        with _lock:  # => only threads that saw None above even attempt to acquire the lock
            if _instance is None:  # => CHECK 2 (locked, slow path): re-checks AFTER acquiring the lock
                _instance = ExpensiveResource()  # => constructs EXACTLY ONCE -- guaranteed by check 2
    return _instance  # => every caller, racing or not, ultimately gets the SAME object


def get_instance_many_times(results: list[ExpensiveResource]) -> None:
    for _ in range(50):  # => calls get_instance() repeatedly from within ONE thread
        results.append(get_instance())  # => each call should return the IDENTICAL object, every time


if __name__ == "__main__":  # => module entry point
    thread_results: list[list[ExpensiveResource]] = [[] for _ in range(8)]  # => one private results list per thread
    threads = [threading.Thread(target=get_instance_many_times, args=(thread_results[i],)) for i in range(8)]  # => 8 threads, all racing to call get_instance() for the FIRST time simultaneously
    for t in threads:  # => starts every thread
        t.start()  # => all 8 threads immediately race into get_instance()'s unlocked first check
    for t in threads:  # => waits for every thread to finish its 50 calls
        t.join()  # => join() blocks until that thread's get_instance_many_times() call returns

    all_instances = [obj for results in thread_results for obj in results]  # => flattens all 8*50=400 results
    unique_instances = {id(obj) for obj in all_instances}  # => unique_instances: distinct object IDENTITIES seen
    print(f"construction_count={construction_count[0]} unique_instances={len(unique_instances)}")
    # => Output: construction_count=1 unique_instances=1

    # => Without CHECK 2 (the SECOND `if _instance is None:`, taken WHILE holding the lock), multiple
    # => threads could all pass CHECK 1 before any of them acquires the lock, and each would construct
    # => its OWN `ExpensiveResource` -- a lost-singleton bug, structurally similar to ex-37's TOCTOU race
    # => (co-08). Re-checking AFTER acquiring the lock (co-11) guarantees construction happens EXACTLY
    # => once, while still letting every SUBSEQUENT call skip the lock entirely via the fast unlocked path.
    assert construction_count[0] == 1  # => confirms ExpensiveResource() ran EXACTLY once, despite 8-way contention
    assert len(unique_instances) == 1  # => confirms every one of the 400 calls returned the SAME object
    print("ex-60 OK")  # => Output: ex-60 OK
