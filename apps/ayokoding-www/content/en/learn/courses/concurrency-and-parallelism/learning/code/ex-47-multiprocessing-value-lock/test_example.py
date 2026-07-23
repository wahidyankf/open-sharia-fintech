"""Example 47: pytest verification for a Lock-Protected `multiprocessing.Value`."""

import multiprocessing

from example import increment_many


def test_shared_value_total_is_exact_across_processes() -> None:
    shared_total = multiprocessing.Value("i", 0)
    processes = [multiprocessing.Process(target=increment_many, args=(shared_total, 1000)) for _ in range(3)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    assert shared_total.value == 3000  # => the built-in lock prevented any lost update across processes


# => Run: pytest -- Output: 1 passed
