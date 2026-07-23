"""Example 32: pytest verification for Livelock -- Both Threads Active, Neither Makes Progress."""

import threading

from example import polite_worker


def test_mutual_politeness_produces_zero_progress() -> None:
    wants_a = [False]
    wants_b = [False]
    barrier = threading.Barrier(2)
    progress = [0]
    t_a = threading.Thread(target=polite_worker, args=(wants_a, wants_b, barrier, progress))
    t_b = threading.Thread(target=polite_worker, args=(wants_b, wants_a, barrier, progress))
    t_a.start()
    t_b.start()
    t_a.join(timeout=2)
    t_b.join(timeout=2)
    assert progress[0] == 0  # => both threads ran every tick but neither ever proceeded
    assert not t_a.is_alive() and not t_b.is_alive()  # => bounded by MAX_TICKS, not a real hang


# => Run: pytest -- Output: 1 passed
