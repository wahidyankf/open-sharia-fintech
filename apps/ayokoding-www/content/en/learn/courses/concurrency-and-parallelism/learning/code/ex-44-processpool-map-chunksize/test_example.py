"""Example 44: pytest verification for `ProcessPoolExecutor.map` chunksize."""

from concurrent.futures import ProcessPoolExecutor

from example import square


def test_chunksize_does_not_change_the_result() -> None:
    data = list(range(200))
    with ProcessPoolExecutor(max_workers=2) as pool:
        default_result = list(pool.map(square, data))
    with ProcessPoolExecutor(max_workers=2) as pool:
        chunked_result = list(pool.map(square, data, chunksize=25))
    expected = [square(n) for n in data]
    assert default_result == expected  # => chunksize=1 (default) matches the serial baseline
    assert chunked_result == expected  # => chunksize=25 also matches -- only the IPC batching differs


# => Run: pytest -- Output: 1 passed
