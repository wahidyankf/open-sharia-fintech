"""Example 1: Big-O Empirical Timing -- Linear vs Quadratic Step Counts."""

# Instead of trusting a formula blindly, COUNT operations directly as n grows
# (co-01) -- counting steps is deterministic, unlike wall-clock timing, which
# jitters with OS scheduling noise on a shared dev machine.


def linear_scan(n: int) -> int:  # => counts steps for a single O(n) pass
    steps = 0  # => steps starts at zero for this call
    for _ in range(n):  # => one iteration per element -- exactly n steps
        steps += 1  # => records one unit of work per iteration
    return steps  # => returns the total step count, not the data itself


def quadratic_scan(n: int) -> int:  # => counts steps for a nested O(n^2) pass
    steps = 0  # => steps starts at zero for this call
    for _ in range(n):  # => outer loop runs n times
        for _ in range(n):  # => inner loop ALSO runs n times, for each outer step
            steps += 1  # => n*n total increments across both loops
    return steps  # => returns the total step count


sizes: list[int] = [10, 20, 40, 80]  # => four sizes, each DOUBLING the last
linear_steps: list[int] = [linear_scan(n) for n in sizes]  # => [10, 20, 40, 80]
quadratic_steps: list[int] = [
    quadratic_scan(n) for n in sizes
]  # => [100, 400, 1600, 6400]
print(linear_steps)  # => Output: [10, 20, 40, 80]
print(quadratic_steps)  # => Output: [100, 400, 1600, 6400]

# Doubling n should roughly DOUBLE an O(n) count and QUADRUPLE an O(n^2) count.
for i in range(1, len(sizes)):  # => walks each consecutive doubling step
    linear_ratio = linear_steps[i] / linear_steps[i - 1]  # => ~2.0 expected
    quad_ratio = quadratic_steps[i] / quadratic_steps[i - 1]  # => ~4.0 expected
    assert 1.9 <= linear_ratio <= 2.1  # => confirms O(n) doubles when n doubles
    assert 3.9 <= quad_ratio <= 4.1  # => confirms O(n^2) quadruples when n doubles
print("ex-01 OK")  # => Output: ex-01 OK
