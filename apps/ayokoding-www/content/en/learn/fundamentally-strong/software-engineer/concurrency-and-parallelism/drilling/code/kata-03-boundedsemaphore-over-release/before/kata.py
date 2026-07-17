"""Kata 3 (before): a plain Semaphore silently accepts an extra release() -- no bug is ever flagged."""

import threading

# => A pool of 2 database connections -- at most 2 callers should ever hold one at a time.
pool = threading.Semaphore(2)  # SMELL: a plain Semaphore, not a BoundedSemaphore


def borrow_connection() -> None:
    pool.acquire()  # => takes one permit -- count drops by 1


def return_connection() -> None:
    pool.release()  # => gives one permit back -- count rises by 1, with NO upper-bound check


borrow_connection()  # => count: 2 -> 1
return_connection()  # => count: 1 -> 2 (correct return)
return_connection()  # BUG: an accidental SECOND release() with no matching acquire() -- count: 2 -> 3
print("both extra release() calls succeeded with no error")

# => The pool's internal permit count is now 3, one MORE than the 2 real connections that exist --
# => a third, and even a fourth, caller can now acquire() a "connection" that was never actually
# => returned to the pool, silently exceeding the pool's real capacity.
first = pool.acquire(blocking=False)  # => succeeds -- count: 3 -> 2
second = pool.acquire(blocking=False)  # => succeeds -- count: 2 -> 1
third = pool.acquire(blocking=False)  # BUG: ALSO succeeds -- there should only be 2 real connections
print(f"first={first} second={second} third={third}")
assert third is True  # => confirms the pool over-granted a THIRD permit that should not exist
print("kata OK (bug reproduced)")
