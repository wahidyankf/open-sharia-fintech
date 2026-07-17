"""Example 24: pytest verification for `submit()` Returns a `Future`; `.result()` Blocks."""

from concurrent.futures import Future, ThreadPoolExecutor

from example import compute


def test_submit_returns_future_and_result_blocks_for_value() -> None:
    with ThreadPoolExecutor(max_workers=1) as pool:
        future: Future[int] = pool.submit(compute, 3, 9)
        assert future.result() == 27  # => .result() waits for and returns the correct value
        assert future.done() is True


# => Run: pytest -- Output: 1 passed
