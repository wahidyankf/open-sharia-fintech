"""Example 78: Three Stated Complexities -- Each Backed by Its Own Doubling Test."""

# A complexity CLAIM (co-01) is only trustworthy once it's TESTED (co-05):
# this example states O(log n), O(n), and O(n log n) for three routines, then
# runs each through a doubling series and checks the step count grows the
# way its stated complexity PREDICTS -- log n adds a constant, n doubles, and
# n log n grows a bit faster than doubling (converging toward 2x as n grows).


def binary_search_steps(n: int) -> int:  # => STATED complexity: O(log n)
    lo, hi = 0, n - 1
    target = n - 1  # => worst case: the target is the LAST element, found last
    steps = 0
    while lo <= hi:  # => each iteration HALVES the remaining search range
        steps += 1
        mid = (lo + hi) // 2
        if mid == target:
            break
        elif mid < target:
            lo = mid + 1  # => discards the lower half
        else:
            hi = mid - 1  # => discards the upper half
    return steps  # => grows by roughly log2(n) -- halving n each step


def linear_steps(n: int) -> int:  # => STATED complexity: O(n)
    steps = 0
    for _ in range(n):  # => exactly one increment per element -- no shortcuts
        steps += 1
    return steps  # => grows EXACTLY proportional to n


def nlogn_steps(n: int) -> int:  # => STATED complexity: O(n log n)
    steps = 0
    for _ in range(n):  # => the OUTER n -- one pass per element
        x = 1
        while x < n:  # => the INNER log n -- doubles x until it reaches n
            x *= 2
            steps += 1
    return steps  # => n independent inner passes, each costing ~log2(n)


sizes: list[int] = [128, 256, 512, 1024]  # => four sizes, each DOUBLING the last

binary_search_counts = [binary_search_steps(n) for n in sizes]
linear_counts = [linear_steps(n) for n in sizes]
nlogn_counts = [nlogn_steps(n) for n in sizes]
print(binary_search_counts)  # => Output: [8, 9, 10, 11]
print(linear_counts)  # => Output: [128, 256, 512, 1024]
print(nlogn_counts)  # => Output: [896, 2048, 4608, 10240]

for i in range(1, len(sizes)):  # => walks each consecutive doubling step
    log_diff = binary_search_counts[i] - binary_search_counts[i - 1]
    linear_ratio = linear_counts[i] / linear_counts[i - 1]
    nlogn_ratio = nlogn_counts[i] / nlogn_counts[i - 1]
    assert log_diff == 1  # => O(log n): doubling n adds EXACTLY one more halving step
    assert 1.9 <= linear_ratio <= 2.1  # => O(n): doubling n DOUBLES the step count
    assert (
        2.1 <= nlogn_ratio <= 2.4
    )  # => O(n log n): doubling n MORE than doubles the count (converging toward 2x)
print("ex-78 OK")  # => Output: ex-78 OK
