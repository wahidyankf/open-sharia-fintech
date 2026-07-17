"""Example 16: pytest verification for `BoundedSemaphore` Catches an Over-Release Bug."""

import threading

from example import release_too_many_times


def test_bounded_semaphore_raises_on_over_release() -> None:
    bounded = threading.BoundedSemaphore(1)
    error = release_too_many_times(bounded, extra_releases=1)
    assert isinstance(error, ValueError)  # => the extra release() is caught, not silently accepted


def test_plain_semaphore_would_not_raise() -> None:
    plain = threading.Semaphore(1)  # => contrast: the non-bounded variant
    plain.acquire()
    plain.release()
    plain.release()  # => an EXTRA release -- a plain Semaphore allows this without error
    assert True  # => reaching this line at all proves no exception was raised above


# => Run: pytest -- Output: 2 passed
