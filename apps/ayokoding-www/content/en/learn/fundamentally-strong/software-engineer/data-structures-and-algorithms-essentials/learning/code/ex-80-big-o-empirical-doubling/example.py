"""Example 80: Empirical Doubling -- Linear vs Binary Search Step Counts."""


# Counts every comparison made -- grows proportionally to len(items) (co-01, co-13).
def linear_search_steps(
    items: list[int], target: int
) -> int:  # => a step-counting scan
    steps = 0  # => tracks how many comparisons this call makes
    for value in items:  # => worst case (target absent) visits EVERY element
        steps += 1  # => one step per element visited
        if value == target:  # => stops counting early once found
            break  # => not hit when target is deliberately absent
    return steps  # => the total number of comparisons made


# Counts every comparison made -- grows proportionally to log2(len(items)) (co-01, co-14).
def binary_search_steps(
    items: list[int], target: int
) -> int:  # => a step-counting search
    steps = 0  # => tracks how many comparisons this call makes
    low, high = 0, len(items) - 1  # => the inclusive range still being searched
    while low <= high:  # => each iteration HALVES the remaining range
        steps += 1  # => one step per range-halving comparison
        mid = (low + high) // 2  # => the midpoint of the current range
        if items[mid] == target:  # => a direct hit
            break  # => not hit when target is deliberately absent
        if items[mid] < target:  # => the midpoint is too small
            low = mid + 1  # => discard the left half
        else:  # => the midpoint is too large
            high = mid - 1  # => discard the right half
    return steps  # => the total number of comparisons made


results: list[tuple[int, int, int]] = []  # => (n, linear_steps, binary_steps) per trial
for n in (1000, 2000, 4000, 8000):  # => n DOUBLES on every trial
    items = list(range(n))  # => a sorted list of n elements
    linear_steps = linear_search_steps(items, target=-1)  # => -1 forces the worst case
    binary_steps = binary_search_steps(items, target=-1)  # => -1 forces the worst case
    results.append(
        (n, linear_steps, binary_steps)
    )  # => records this trial for the asserts below
    print(f"n={n}: linear={linear_steps}, binary={binary_steps}")
    # => Output (n=1000): n=1000: linear=1000, binary=9
    # => Output (n=2000): n=2000: linear=2000, binary=10
    # => Output (n=4000): n=4000: linear=4000, binary=11
    # => Output (n=8000): n=8000: linear=8000, binary=12

# linear steps double right alongside n; binary steps grow by roughly +1 each doubling.
assert (
    results[1][1] == 2 * results[0][1]
)  # => confirms linear steps EXACTLY double with n
assert (
    results[1][2] - results[0][2] <= 2
)  # => confirms binary steps grow by only ~1 per doubling
print("ex-80 OK")  # => Output: ex-80 OK
