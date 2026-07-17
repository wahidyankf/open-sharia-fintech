"""Example 13: `RLock` Lets the Owning Thread Re-Acquire."""

import threading  # => threading.RLock is the reentrant sibling of threading.Lock (co-12)


def outer(rlock: threading.RLock, log: list[str]) -> None:  # => acquires, then calls inner() -- SAME thread
    with rlock:  # => first acquire -- succeeds immediately, no other holder yet
        log.append("outer-acquired")  # => proves the first acquire succeeded
        inner(rlock, log)  # => calls a function that acquires the SAME rlock AGAIN


def inner(rlock: threading.RLock, log: list[str]) -> None:  # => called WHILE outer() still holds rlock
    with rlock:  # => a SECOND acquire, by the SAME thread that already holds it -- this is the point
        log.append("inner-acquired")  # => only reached if RLock allowed the re-entrant acquire


if __name__ == "__main__":  # => module entry point
    rl = threading.RLock()  # => one RLock, tracking BOTH an owning thread and an acquire COUNT
    events: list[str] = []  # => records the order acquisitions actually happened in
    outer(rl, events)  # => outer() acquires once, then inner() acquires again -- same thread, no hang
    print(events)  # => Output: ['outer-acquired', 'inner-acquired']

    # => A plain threading.Lock would DEADLOCK here (ex-14 demonstrates exactly that): the second
    # => acquire() call would block forever waiting for a lock the SAME thread already holds.
    # => RLock tracks the owning thread and a re-entrancy count, so the SAME thread may acquire it
    # => repeatedly without blocking -- each acquire() needs a matching release() to fully unlock.
    assert events == ["outer-acquired", "inner-acquired"]  # => confirms BOTH acquires succeeded
    print("ex-13 OK")  # => Output: ex-13 OK
