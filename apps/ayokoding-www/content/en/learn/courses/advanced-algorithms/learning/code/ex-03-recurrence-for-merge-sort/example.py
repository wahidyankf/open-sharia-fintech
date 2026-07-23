"""Example 3: Unroll T(n) = 2T(n/2) + n into the Closed Form n*log2(n) + n."""

# Merge sort splits into 2 halves (the "2T(n/2)") and does O(n) work to merge
# them back (the "+n") (co-03). Unrolling k levels gives T(n) = kn + 2^k*T(n/2^k);
# stopping when n/2^k == 1 sets k = log2(n), so T(n) = n*log2(n) + n*T(1).


def recurrence_t(n: int) -> int:  # => computes T(n) directly from the recurrence
    if n == 1:  # => base case: T(1) = 1, one unit of work on a single element
        return 1  # => stops the recursion at the smallest subproblem
    return 2 * recurrence_t(n // 2) + n  # => 2T(n/2) [two halves] + n [merge cost]


def closed_form(n: int) -> int:  # => the algebraically-unrolled formula
    log2_n = n.bit_length() - 1  # => exact log2(n) via bit-length, for powers of two
    return n * log2_n + n  # => n*log2(n) [merge levels] + n [T(1) base-case work]


sizes: list[int] = [2, 4, 8, 16, 32]  # => powers of two, so bit_length gives exact log2
for n in sizes:  # => checks the recurrence against its closed form at each size
    via_recurrence = recurrence_t(n)  # => direct recursive evaluation
    via_formula = closed_form(n)  # => the unrolled, non-recursive formula
    print(f"n={n}: recurrence={via_recurrence}, closed_form={via_formula}")
    # => Output: one "n=..., recurrence=..., closed_form=..." line per size, EQUAL
    assert (
        via_recurrence == via_formula
    )  # => confirms the unrolled formula matches the recurrence exactly
print("ex-03 OK")  # => Output: ex-03 OK
