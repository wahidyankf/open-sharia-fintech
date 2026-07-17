"""Example 18: pytest verification for A `Barrier` Rendezvous Point."""

import threading

from example import PARTIES, arrive


def test_no_thread_passes_until_all_arrive() -> None:
    barrier = threading.Barrier(PARTIES)
    order: list[int] = []
    delays = [0.02, 0.06, 0.10, 0.14]
    threads = [threading.Thread(target=arrive, args=(barrier, order, i, delays[i])) for i in range(PARTIES)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(order) == list(range(PARTIES))  # => all four eventually passed the rendezvous


# => Run: pytest -- Output: 1 passed
