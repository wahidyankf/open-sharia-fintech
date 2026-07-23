"""Example 74: pytest verification for State Fault-Line Case Study."""

import threading

from example import SharedMutableCounter, partial_sum, racy_increment


def test_shared_mutable_design_reproduces_a_lost_update_race() -> None:
    counter = SharedMutableCounter()  # => fresh counter, isolated from the module-level demo
    event_a_read = threading.Event()
    event_b_read = threading.Event()
    thread_a = threading.Thread(target=racy_increment, args=(counter, event_a_read, event_b_read))
    thread_b = threading.Thread(target=racy_increment, args=(counter, event_b_read, event_a_read))
    thread_a.start()
    thread_b.start()
    thread_a.join()
    thread_b.join()
    # => two increments were attempted, but the forced interleaving guarantees only one survives
    assert counter.value == 1  # => NOT 2 -- this is the race, reproduced deterministically every run


def test_immutable_design_has_no_shared_target_to_race_on() -> None:
    results: list[int] = [0, 0]  # => disjoint per-thread slots, exactly like the module-level demo

    def run_partial(index: int, nums: tuple[int, ...]) -> None:
        results[index] = partial_sum(nums)

    threads = [
        threading.Thread(target=run_partial, args=(0, (1, 2, 3))),
        threading.Thread(target=run_partial, args=(1, (4, 5, 6))),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sum(results) == 21  # => 1+2+3+4+5+6, correct regardless of thread scheduling order


# => Run: pytest -- Output: 2 passed
