"""Example 60: pytest verification for Double-Checked-Locking Singleton Construction."""

import threading

from example import ExpensiveResource, construction_count, get_instance_many_times


def test_singleton_constructed_exactly_once_under_thread_contention() -> None:
    thread_results: list[list[ExpensiveResource]] = [[] for _ in range(6)]
    threads = [threading.Thread(target=get_instance_many_times, args=(thread_results[i],)) for i in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    all_instances = [obj for results in thread_results for obj in results]
    unique_instances = {id(obj) for obj in all_instances}
    assert construction_count[0] == 1  # => ExpensiveResource() ran exactly once, despite 6-way contention
    assert len(unique_instances) == 1  # => every call returned the same object


# => Run: pytest -- Output: 1 passed
