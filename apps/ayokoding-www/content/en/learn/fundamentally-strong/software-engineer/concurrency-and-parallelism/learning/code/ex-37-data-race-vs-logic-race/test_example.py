"""Example 37: pytest verification for Data Race vs Logic Race."""

import threading

from example import WITHDRAWALS, data_race_decrement, logic_race_withdraw


def test_data_race_loses_updates() -> None:
    balance = [0]
    t1 = threading.Thread(target=data_race_decrement, args=(balance, WITHDRAWALS))
    t2 = threading.Thread(target=data_race_decrement, args=(balance, WITHDRAWALS))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert balance[0] > -2 * WITHDRAWALS  # => the unsynchronized read-modify-write lost at least one decrement


def test_logic_race_overdraws_despite_individually_locked_statements() -> None:
    balance = [100]
    guard = threading.Lock()
    successes = [0]
    checked_barrier = threading.Barrier(2)
    t1 = threading.Thread(target=logic_race_withdraw, args=(balance, 100, guard, successes, checked_barrier))
    t2 = threading.Thread(target=logic_race_withdraw, args=(balance, 100, guard, successes, checked_barrier))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert balance[0] < 0  # => both threads' checks passed before either write landed -- an overdraft
    assert successes[0] == 2  # => both "succeeded" from each thread's own point of view


# => Run: pytest -- Output: 2 passed
