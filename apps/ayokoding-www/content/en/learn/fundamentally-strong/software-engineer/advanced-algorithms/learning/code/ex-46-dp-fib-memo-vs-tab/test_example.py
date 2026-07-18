"""Example 46: pytest verification for Memoized vs Tabulated Fibonacci."""

from example import fib_memo, fib_tab


def test_both_styles_agree_across_many_inputs() -> None:
    for n in range(25):
        assert fib_memo(n) == fib_tab(n)


def test_known_fibonacci_values() -> None:
    assert fib_tab(0) == 0
    assert fib_tab(1) == 1
    assert fib_tab(10) == 55


# => Run: pytest -- Output: 2 passed
