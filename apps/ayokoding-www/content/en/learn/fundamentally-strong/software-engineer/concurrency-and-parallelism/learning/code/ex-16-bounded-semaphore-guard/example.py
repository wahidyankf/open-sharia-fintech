"""Example 16: `BoundedSemaphore` Catches an Over-Release Bug."""

import threading  # => threading.BoundedSemaphore -- a Semaphore that guards against extra release()s


def release_too_many_times(sem: threading.BoundedSemaphore, extra_releases: int) -> Exception | None:
    # => acquires once, then releases MORE times than it acquired -- a common bookkeeping bug
    sem.acquire()  # => acquires the single permit -- count now 0
    sem.release()  # => releases it back -- count now 1, matching the original acquire()
    caught: Exception | None = None  # => caught: will hold the ValueError, if one is raised
    try:  # => the EXTRA release() calls below have no matching acquire()
        for _ in range(extra_releases):  # => calls release() again, with nothing left to release
            sem.release()  # => a plain Semaphore would silently grow past its intended maximum
    except ValueError as exc:  # => BoundedSemaphore specifically detects and rejects this
        caught = exc  # => caught now holds the raised exception, for the caller to inspect
    return caught  # => None would mean the bug went undetected -- BoundedSemaphore prevents that


if __name__ == "__main__":  # => module entry point
    bounded = threading.BoundedSemaphore(1)  # => a semaphore that must never exceed its initial value
    error = release_too_many_times(bounded, extra_releases=1)  # => triggers exactly one extra release()
    print(f"error_type={type(error).__name__ if error else None}")  # => Output: error_type=ValueError

    # => A plain threading.Semaphore would accept the extra release() silently, letting its internal
    # => counter drift above the number of resources that actually exist -- a bug that then lets
    # => MORE threads through a "limit N concurrent" section (ex-15) than the resource can handle.
    # => BoundedSemaphore raises ValueError the instant release() would exceed the initial count.
    assert error is not None  # => confirms the over-release was CAUGHT, not silently accepted
    assert isinstance(error, ValueError)  # => confirms it's specifically the documented ValueError
    print("ex-16 OK")  # => Output: ex-16 OK
