"""Example 63: pytest verification for a Single-Owner, Lock-Free Counter."""

import queue
import threading

from example import client, owner


def test_single_owner_counter_is_exact_with_no_lock() -> None:
    requests: "queue.Queue[int | None]" = queue.Queue()
    total = [0]
    owner_thread = threading.Thread(target=owner, args=(requests, total))
    owner_thread.start()

    clients = [threading.Thread(target=client, args=(requests, 200)) for _ in range(3)]
    for c in clients:
        c.start()
    for c in clients:
        c.join()

    requests.put(None)
    owner_thread.join()

    assert total[0] == 600  # => 3 clients * 200 requests each, exact -- no lock needed, no lost updates


# => Run: pytest -- Output: 1 passed
