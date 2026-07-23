"""Example 4: The Master Theorem's Three Cases, One Recurrence Each."""

# For T(n) = a*T(n/b) + f(n), compare f(n) against n^(log_b a) (co-04, co-03):
# Case 1: f(n) grows SLOWER -> the recursive splits dominate, T(n) = Theta(n^log_b a).
# Case 2: f(n) grows at the SAME rate -> T(n) = Theta(n^log_b a * log n).
# Case 3: f(n) grows FASTER -> the combine step dominates, T(n) = Theta(f(n)).
import math  # => needed for math.log to compute log_b(a) for non-power exponents


def critical_exponent(a: int, b: int) -> float:  # => computes log_b(a), the split cost
    return math.log(a) / math.log(b)  # => change-of-base: log_b(a) = ln(a)/ln(b)


def classify_master_case(
    a: int, b: int, f_exponent: float
) -> str:  # => a,b from a*T(n/b)+f(n); f_exponent is f(n)'s polynomial degree
    crit = critical_exponent(a, b)  # => n^crit is the "split work" baseline
    if f_exponent < crit - 1e-9:  # => f(n) grows strictly slower than n^crit
        return "case1"  # => split work dominates: Theta(n^log_b(a))
    if abs(f_exponent - crit) < 1e-9:  # => f(n) matches n^crit exactly
        return "case2"  # => balanced: Theta(n^log_b(a) * log n)
    return "case3"  # => f(n) grows strictly faster: Theta(f(n))


# Recurrence 1: T(n) = 8T(n/2) + n  -- binary-search-like split, linear combine.
# log_2(8) = 3, f(n)=n has exponent 1 < 3 -- the 8-way split dominates (Case 1).
case1_recurrence = classify_master_case(
    a=8, b=2, f_exponent=1
)  # => the recursive calls outweigh the combine step
print(f"T(n)=8T(n/2)+n is {case1_recurrence}")  # => Output: ... is case1

# Recurrence 2: T(n) = 2T(n/2) + n  -- exactly merge sort's recurrence (co-07).
# log_2(2) = 1, f(n)=n has exponent 1 == 1 -- split and combine balance (Case 2).
case2_recurrence = classify_master_case(
    a=2, b=2, f_exponent=1
)  # => matches Example 3's n*log2(n) result
print(f"T(n)=2T(n/2)+n is {case2_recurrence}")  # => Output: ... is case2

# Recurrence 3: T(n) = 2T(n/2) + n^2  -- a quadratic combine step dwarfs the split.
# log_2(2) = 1, f(n)=n^2 has exponent 2 > 1 -- the combine step dominates (Case 3).
case3_recurrence = classify_master_case(
    a=2, b=2, f_exponent=2
)  # => the O(n^2) combine step is the bottleneck, not the recursion
print(f"T(n)=2T(n/2)+n^2 is {case3_recurrence}")  # => Output: ... is case3

assert case1_recurrence == "case1"  # => 8-way split beats a linear combine
assert case2_recurrence == "case2"  # => merge sort: split and combine balance
assert case3_recurrence == "case3"  # => quadratic combine dominates the recursion
print("ex-04 OK")  # => Output: ex-04 OK
