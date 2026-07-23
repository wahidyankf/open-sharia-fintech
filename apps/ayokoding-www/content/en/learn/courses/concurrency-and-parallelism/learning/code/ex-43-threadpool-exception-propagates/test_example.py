"""Example 43: pytest verification for Exception Propagation Through `Future.result()`."""

from concurrent.futures import ThreadPoolExecutor

import pytest

from example import InsufficientFundsError, risky_withdrawal


def test_successful_task_returns_normally() -> None:
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(risky_withdrawal, 100, 30)
        assert future.result() == 70  # => a plain int, no exception, on the success path


def test_failing_task_reraises_on_result() -> None:
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(risky_withdrawal, 100, 500)
        with pytest.raises(InsufficientFundsError):
            future.result()  # => .result() is where the worker's exception surfaces, re-raised


# => Run: pytest -- Output: 2 passed
