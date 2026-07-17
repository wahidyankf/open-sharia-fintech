"""Example 78: Three Stated Complexities -- Each Backed by Its Own Doubling Test."""

# A complexity CLAIM (co-01) is only trustworthy once it's TESTED (co-05):
# this example states O(log n), O(n), and O(n log n) for three routines, then
# runs each through a doubling series and checks the step count grows the
# way its stated complexity PREDICTS -- log n adds a constant, n doubles, and
# n log n grows a bit faster than doubling (converging toward 2x as n grows).


def binary_search_steps(n: int) -> int:  # => STATED complexity: O(log n)
    lo, hi = 0, n - 1  # => the initial search bounds
    target = n - 1  # => worst case: the target is the LAST element, found last
    steps = 0  # => counts iterations, not elements touched
    while lo <= hi:  # => each iteration HALVES the remaining search range
        steps += 1  # => one more halving step taken
        mid = (lo + hi) // 2  # => the midpoint of the current range
        if mid == target:  # => found it -- worst case, this happens LAST
            break  # => stops counting once found
        elif mid < target:  # => target must be further right
            lo = mid + 1  # => discards the lower half
        else:  # => target must be further left
            hi = mid - 1  # => discards the upper half
    return steps  # => grows by roughly log2(n) -- halving n each step


def linear_steps(n: int) -> int:  # => STATED complexity: O(n)
    steps = 0  # => counts one increment per element
    for _ in range(n):  # => exactly one increment per element -- no shortcuts
        steps += 1  # => one unit of work per element, no better no worse
    return steps  # => grows EXACTLY proportional to n


def nlogn_steps(n: int) -> int:  # => STATED complexity: O(n log n)
    steps = 0  # => counts every inner-loop iteration, across all outer passes
    for _ in range(n):  # => the OUTER n -- one pass per element
        x = 1  # => resets the doubling counter for this outer pass
        while x < n:  # => the INNER log n -- doubles x until it reaches n
            x *= 2  # => the doubling step
            steps += 1  # => one more inner iteration counted
    return steps  # => n independent inner passes, each costing ~log2(n)


sizes: list[int] = [128, 256, 512, 1024]  # => four sizes, each DOUBLING the last

binary_search_counts = [  # => opens the O(log n) step-count collection
    binary_search_steps(n)  # => this size's own worst-case step count
    for n in sizes  # => this size's own step count
]  # => O(log n) step counts
linear_counts = [linear_steps(n) for n in sizes]  # => O(n) step counts
nlogn_counts = [nlogn_steps(n) for n in sizes]  # => O(n log n) step counts
print(binary_search_counts)  # => Output: [8, 9, 10, 11]
print(linear_counts)  # => Output: [128, 256, 512, 1024]
print(nlogn_counts)  # => Output: [896, 2048, 4608, 10240]

for i in range(1, len(sizes)):  # => walks each consecutive doubling step
    log_diff = (  # => opens the O(log n) step-count difference
        binary_search_counts[i] - binary_search_counts[i - 1]
    )  # => growth in step count
    linear_ratio = (  # => opens the O(n) step-count ratio
        linear_counts[i] / linear_counts[i - 1]
    )  # => growth ratio, not difference
    nlogn_ratio = (  # => opens the O(n log n) step-count ratio
        nlogn_counts[i] / nlogn_counts[i - 1]
    )  # => growth ratio, not difference
    assert log_diff == 1  # => O(log n): doubling n adds EXACTLY one more halving step
    assert 1.9 <= linear_ratio <= 2.1  # => O(n): doubling n DOUBLES the step count
    assert (  # => opens the O(n log n) growth-rate check
        2.1 <= nlogn_ratio <= 2.4
    )  # => O(n log n): doubling n MORE than doubles the count (converging toward 2x)
print("ex-78 OK")  # => Output: ex-78 OK
