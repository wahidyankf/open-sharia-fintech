"""Example 66: pytest verification for A Trampoline Simulating Tail-Call Optimization."""

from example import sum_to_n_trampolined, trampoline


def test_trampoline_handles_depth_that_would_break_plain_recursion() -> None:
    deep_n = 50_000
    result = trampoline(sum_to_n_trampolined(deep_n))
    assert result == deep_n * (deep_n + 1) // 2


# => Run: pytest -- Output: 1 passed
