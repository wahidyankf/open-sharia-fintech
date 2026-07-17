"""Example 74: pytest verification for the `while not predicate:` Condition Loop Pattern."""

import threading
import time

from example import waiter_with_if, waiter_with_while


def test_if_pattern_proceeds_on_a_premature_notify_while_loop_pattern_does_not() -> None:
    cond = threading.Condition()
    ready: list[bool] = [False]
    if_results: list[bool] = []
    while_results: list[bool] = []
    if_started = threading.Event()
    while_started = threading.Event()

    if_thread = threading.Thread(target=waiter_with_if, args=(cond, ready, if_results, if_started))
    while_thread = threading.Thread(target=waiter_with_while, args=(cond, ready, while_results, while_started))
    if_thread.start()
    while_thread.start()
    if_started.wait(timeout=2)
    while_started.wait(timeout=2)
    time.sleep(0.05)

    with cond:
        cond.notify_all()  # => a premature notification -- ready[0] is still False here
    time.sleep(0.05)

    with cond:
        ready[0] = True
        cond.notify_all()  # => the genuine notification

    if_thread.join(timeout=2)
    while_thread.join(timeout=2)

    assert if_results == [False]  # => the buggy if-pattern proceeded on a stale, incorrect value
    assert while_results == [True]  # => the correct while-pattern only proceeded once genuinely ready


# => Run: pytest -- Output: 1 passed
