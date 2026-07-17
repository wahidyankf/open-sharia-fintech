"""Example 36: pytest verification for Any Read-Modify-Write Needs a Lock."""

import threading

from example import deposit_no_lock, deposit_with_lock


def test_unsynchronized_deposits_lose_updates_under_load() -> None:
    amounts_a = [2] * 300
    amounts_b = [3] * 300
    balance = [0]
    t1 = threading.Thread(target=deposit_no_lock, args=(balance, amounts_a))
    t2 = threading.Thread(target=deposit_no_lock, args=(balance, amounts_b))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    expected = sum(amounts_a) + sum(amounts_b)
    assert balance[0] < expected  # => lost at least one deposit to the unsynchronized race


def test_locked_deposits_are_always_exact() -> None:
    amounts_a = [5] * 300
    amounts_b = [7] * 300
    balance = [0]
    lock = threading.Lock()
    t1 = threading.Thread(target=deposit_with_lock, args=(balance, amounts_a, lock))
    t2 = threading.Thread(target=deposit_with_lock, args=(balance, amounts_b, lock))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    expected = sum(amounts_a) + sum(amounts_b)
    assert balance[0] == expected  # => the lock protects the entire read-modify-write, no losses


# => Run: pytest -- Output: 2 passed
