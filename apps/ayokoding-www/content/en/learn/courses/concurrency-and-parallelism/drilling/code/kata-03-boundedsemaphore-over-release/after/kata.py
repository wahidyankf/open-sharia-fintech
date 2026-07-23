"""Kata 3 (after): a BoundedSemaphore raises immediately on an extra release() -- the bug is caught."""

import threading

# => The SAME 2-connection pool, now using BoundedSemaphore -- FIX: it tracks the INITIAL count and
# => refuses any release() that would push the permit count above it.
pool = threading.BoundedSemaphore(2)


def borrow_connection() -> None:
    pool.acquire()


def return_connection() -> None:
    pool.release()


borrow_connection()  # => count: 2 -> 1
return_connection()  # => count: 1 -> 2 (correct return)
try:
    return_connection()  # => an accidental SECOND release() -- BoundedSemaphore refuses it
except ValueError as exc:
    print(f"blocked: {exc}")  # => Output: blocked: Semaphore released too many times
else:
    raise AssertionError("expected the extra release() to raise ValueError")

# => The pool's permit count is still correctly 2 -- exactly matching the 2 real connections.
first = pool.acquire(blocking=False)  # => succeeds -- count: 2 -> 1
second = pool.acquire(blocking=False)  # => succeeds -- count: 1 -> 0
third = pool.acquire(blocking=False)  # => correctly FAILS -- no third real connection exists
print(f"first={first} second={second} third={third}")
assert third is False  # => confirms the pool never over-grants beyond its real capacity
print("kata OK (fix verified)")
