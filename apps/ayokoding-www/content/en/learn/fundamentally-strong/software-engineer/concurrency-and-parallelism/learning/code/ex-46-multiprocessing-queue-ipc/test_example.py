"""Example 46: pytest verification for `multiprocessing.Queue` Cross-Process IPC."""

import multiprocessing

from example import produce_in_child


def test_items_cross_the_process_boundary_in_order() -> None:
    q: "multiprocessing.Queue[int]" = multiprocessing.Queue()
    child = multiprocessing.Process(target=produce_in_child, args=(q,))
    child.start()

    received: list[int] = []
    while True:
        item = q.get()
        if item == -1:
            break
        received.append(item)
    child.join()

    assert received == [i * i for i in range(10)]  # => every item genuinely crossed the process boundary


# => Run: pytest -- Output: 1 passed
