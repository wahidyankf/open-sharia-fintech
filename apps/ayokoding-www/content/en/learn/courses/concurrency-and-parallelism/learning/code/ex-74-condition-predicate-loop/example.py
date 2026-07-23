"""Example 74: `while not predicate: cond.wait()` -- Guarding Against a Spurious/Early Wakeup."""

import threading  # => co-14: the SAME Condition primitive as ex-19, ex-41, ex-61
import time  # => gives each waiter thread time to genuinely register inside cond.wait()


def waiter_with_if(cond: threading.Condition, ready: list[bool], results: list[bool], started: threading.Event) -> None:
    with cond:  # => acquires the Condition's lock
        started.set()  # => signals the main thread that THIS waiter is about to call wait()
        if not ready[0]:  # => a SINGLE `if` check -- the BUGGY pattern this example warns against
            cond.wait()  # => sleeps until notified -- but does NOT re-check `ready` after waking up
        results.append(ready[0])  # => proceeds REGARDLESS of whether `ready[0]` is ACTUALLY True by now


def waiter_with_while(cond: threading.Condition, ready: list[bool], results: list[bool], started: threading.Event) -> None:
    with cond:  # => acquires the SAME Condition's lock
        started.set()  # => signals the main thread that THIS waiter is about to call wait()
        while not ready[0]:  # => a WHILE loop -- the CORRECT pattern (co-14)
            cond.wait()  # => sleeps until notified, then RE-CHECKS the predicate before proceeding
        results.append(ready[0])  # => only reaches here once `ready[0]` is GENUINELY True


if __name__ == "__main__":  # => module entry point
    cond = threading.Condition()  # => cond: shared by both waiter threads AND the main thread's notifications
    ready: list[bool] = [False]  # => ready[0]: the ACTUAL predicate both waiters are waiting on
    if_results: list[bool] = []  # => if_results: filled in by the buggy `if`-based waiter
    while_results: list[bool] = []  # => while_results: filled in by the correct `while`-based waiter
    if_started = threading.Event()  # => if_started: set once the `if`-waiter has entered its critical section
    while_started = threading.Event()  # => while_started: set once the `while`-waiter has entered its

    if_thread = threading.Thread(target=waiter_with_if, args=(cond, ready, if_results, if_started))
    while_thread = threading.Thread(target=waiter_with_while, args=(cond, ready, while_results, while_started))
    if_thread.start()  # => starts the buggy waiter
    while_thread.start()  # => starts the correct waiter
    if_started.wait(timeout=2)  # => waits for the `if`-waiter to actually reach `cond.wait()`
    while_started.wait(timeout=2)  # => waits for the `while`-waiter to actually reach `cond.wait()`
    time.sleep(0.05)  # => a small margin to be confident BOTH threads are genuinely blocked inside wait()

    with cond:  # => the main thread now sends a PREMATURE notification -- `ready[0]` is STILL False here
        cond.notify_all()  # => wakes BOTH waiters -- simulating a spurious wakeup / an early notify()

    time.sleep(0.05)  # => gives the woken threads time to react to the premature notification above

    with cond:  # => now the main thread makes the predicate GENUINELY true
        ready[0] = True  # => flips the ACTUAL condition both waiters are supposed to be waiting for
        cond.notify_all()  # => wakes both waiters again -- THIS time the predicate really holds

    if_thread.join(timeout=2)  # => waits for the buggy waiter to finish
    while_thread.join(timeout=2)  # => waits for the correct waiter to finish

    print(f"if_results={if_results} while_results={while_results}")  # => Output: if_results=[False] while_results=[True]

    # => The premature `notify_all()` above wakes BOTH waiters even though `ready[0]` is still False.
    # => The `if`-based waiter has no way to notice this -- it already passed its ONE check, so it
    # => proceeds with a WRONG value. The `while`-based waiter re-checks the predicate every time it
    # => wakes (co-14): finding it still False, it calls `cond.wait()` again, and only proceeds once
    # => `ready[0]` is genuinely True. This is why EVERY `Condition.wait()` call belongs inside a
    # => `while`, never a plain `if` -- spurious wakeups are a documented possibility, not a corner case.
    assert if_results == [False]  # => confirms the buggy `if` pattern proceeded on a STALE, incorrect value
    assert while_results == [True]  # => confirms the correct `while` pattern only proceeded once genuinely ready
    print("ex-74 OK")  # => Output: ex-74 OK
