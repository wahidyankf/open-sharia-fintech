"""Example 30: A Global Lock Order Fixes the Deadlock."""

import threading  # => co-18: lock-ordering discipline -- the fix for ex-29's circular wait
import time  # => used only for a small sleep that guarantees genuine contention below, not luck


def thread_a(lock_a: threading.Lock, lock_b: threading.Lock, holding_a: threading.Event) -> None:
    with lock_a:  # => acquires lock_a FIRST -- same order thread_b will use below
        holding_a.set()  # => signal thread_b it can now genuinely try to acquire lock_a and block on it
        time.sleep(0.05)  # => hold lock_a briefly so thread_b's acquisition attempt provably contends
        with lock_b:  # => acquires lock_b SECOND -- no one else can hold lock_b while wanting lock_a here
            pass  # => reached every time: with a single order, no thread can form the opposite wait


def thread_b(lock_a: threading.Lock, lock_b: threading.Lock, holding_a: threading.Event) -> None:
    holding_a.wait()  # => wait until thread_a is DEFINITELY inside its `with lock_a:` block
    with lock_a:  # => acquires lock_a FIRST too -- the FIX: identical order to thread_a, not reversed
        with lock_b:  # => acquires lock_b SECOND -- same order as thread_a, so the cycle can't form
            pass  # => reached every time: this thread simply waited its turn for lock_a, then proceeded


def no_longer_deadlocks() -> tuple[bool, bool]:  # => returns (a_finished, b_finished)
    lock_a = threading.Lock()  # => resource A -- ALWAYS acquired first by both threads now
    lock_b = threading.Lock()  # => resource B -- ALWAYS acquired second by both threads now
    holding_a = threading.Event()  # => NOT a Barrier -- a Barrier here would itself deadlock (see Discussion)
    t_a = threading.Thread(target=thread_a, args=(lock_a, lock_b, holding_a))
    t_b = threading.Thread(target=thread_b, args=(lock_a, lock_b, holding_a))
    t_a.start()  # => starts thread_a -- acquires lock_a, signals, briefly holds it, then wants lock_b
    t_b.start()  # => starts thread_b -- waits for the signal, then genuinely blocks trying to get lock_a
    t_a.join(timeout=2)  # => a generous but FINITE timeout -- a real fix returns well before this
    t_b.join(timeout=2)  # => same bound for thread_b
    return not t_a.is_alive(), not t_b.is_alive()  # => True, True means BOTH finished -- no deadlock


if __name__ == "__main__":  # => module entry point
    a_done, b_done = no_longer_deadlocks()  # => a_done/b_done: did each thread actually complete?
    print(f"a_done={a_done} b_done={b_done}")  # => Output: a_done=True b_done=True

    # => Both threads now acquire lock_a BEFORE lock_b -- a single, consistent GLOBAL ORDER. With
    # => only one possible acquisition order, no thread can ever hold lock_b while waiting on
    # => lock_a held by another thread that itself wants lock_b -- the circular wait is impossible.
    # => Note this deliberately uses an `Event`, not a `Barrier`, to force the contention: a Barrier
    # => would require BOTH threads to reach it WHILE holding lock_a, but only one thread can hold
    # => lock_a at a time once the order is fixed -- the second thread would block trying to acquire
    # => lock_a before it could ever reach the barrier, hanging forever. That's not a flaw in the
    # => fix; it is exactly the point: under one global order there is only ONE thread inside the
    # => critical section at a time, by design -- an `Event` correctly captures "wait your turn",
    # => where a `Barrier` incorrectly demands "arrive at the same moment", which is now impossible.
    assert a_done is True  # => confirms thread_a completed, not hung
    assert b_done is True  # => confirms thread_b completed, not hung
    print("ex-30 OK")  # => Output: ex-30 OK
