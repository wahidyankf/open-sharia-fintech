"""Example 42: pytest verification for A Parameterized @retry(3) Decorator."""

from example import retry


def test_retry_stops_as_soon_as_the_wrapped_call_succeeds() -> None:
    attempts: list[int] = []

    @retry(5)
    def sometimes_fails() -> str:
        attempts.append(len(attempts) + 1)
        if len(attempts) < 2:
            raise ValueError("not yet")
        return "ok"

    assert sometimes_fails() == "ok"
    assert attempts == [1, 2]  # => stopped retrying the moment it succeeded


# => Run: pytest -- Output: 1 passed
