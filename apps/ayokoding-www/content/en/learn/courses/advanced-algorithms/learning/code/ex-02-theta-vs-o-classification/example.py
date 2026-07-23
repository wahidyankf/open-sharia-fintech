"""Example 2: Classify Growth Rates into Theta/Big-O Buckets via a Doubling Test."""

# O is an UPPER bound, Omega a LOWER bound, and Theta a TIGHT bound that is
# both at once (co-01) -- a doubling test tells buckets apart empirically:
# doubling n roughly multiplies an O(n^k) count by 2^k.
from collections.abc import Callable  # => the real generic-callable type, not a string


def constant_cost(n: int) -> int:  # => models Theta(1): touches ONE element
    return 1  # => n never influences the step count at all


def linear_cost(n: int) -> int:  # => models Theta(n): touches every element once
    return n  # => step count grows exactly proportionally to n


def quadratic_cost(n: int) -> int:  # => models Theta(n^2): a full pairwise scan
    return n * n  # => step count grows with the SQUARE of n


# doubling_ratio(f) returns how much f(n) multiplies when n doubles from 100 to 200.
def doubling_ratio(f: Callable[[int], int]) -> float:  # => generic over any cost fn
    before = f(100)  # => cost at the smaller size
    after = f(200)  # => cost at DOUBLE the size
    return after / before  # => the empirical multiplier this doubling caused


classifications: dict[str, float] = {  # => maps a human label to its measured ratio
    "constant (Theta(1))": doubling_ratio(  # => key names the bucket under test
        constant_cost  # => the zero-growth function passed as the callback
    ),  # => expect ~1.0 -- unaffected by n
    "linear (Theta(n))": doubling_ratio(linear_cost),  # => expect ~2.0
    "quadratic (Theta(n^2))": doubling_ratio(quadratic_cost),  # => expect ~4.0
}  # => closes the dict -- exactly 3 entries, one per growth bucket
for label, ratio in classifications.items():  # => walks all three buckets
    print(f"{label}: {ratio:.2f}")  # => Output: one "label: ratio" line per bucket

assert (  # => opens a parenthesized assert so the long condition can wrap
    classifications["constant (Theta(1))"] == 1.0  # => True iff the ratio was exact
)  # => confirms O(1) is untouched by n doubling
assert classifications["linear (Theta(n))"] == 2.0  # => confirms O(n) exactly doubles
assert (
    classifications["quadratic (Theta(n^2))"] == 4.0
)  # => confirms O(n^2) exactly quadruples
print("ex-02 OK")  # => Output: ex-02 OK
