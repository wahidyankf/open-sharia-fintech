"""Kata 8 (before): naive recursive Fibonacci re-solves the SAME subproblem exponentially many times."""

calls = 0


def fib(n: int) -> int:
    global calls
    calls += 1
    if n <= 1:
        return n
    return fib(n - 1) + fib(
        n - 2
    )  # BUG: no cache -- fib(n - 2) is fully re-computed inside fib(n - 1) too


result = fib(25)
print(result)
print(calls)
print(
    calls > 100_000
)  # naive fib(25) calls itself 242,785 times for a result that needs only 25 additions
