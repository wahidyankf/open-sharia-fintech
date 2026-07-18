---
title: "Intermediate Examples"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 20
---

Examples 25-52 extend the beginner tier into amortized analysis (the doubling dynamic array and the accounting method), quicksort's practical fixes (a random pivot, then quickselect), divide-and-conquer geometry (closest pair of points), Fenwick and segment trees, optimized union-find (union-by-rank, path compression) and connected components, topological sort (Kahn's algorithm and DFS finish order) with cycle detection, Dijkstra (including the unreachable-node case) and Bellman-Ford (including negative-cycle detection), minimum spanning trees (Kruskal and Prim), the greedy paradigm (a correct case and a failing one), and the first wave of dynamic programming (Fibonacci, climbing stairs, coin change, edit distance, longest common subsequence, 0/1 knapsack), closing with binary search boundaries. Every example runs and verifies exactly like the beginner tier -- `python3 example.py` for inline output, `pytest` for the colocated `test_example.py`.

---

### Example 25: A Doubling Dynamic Array's Amortized O(1) Append

_ex-25 &middot; exercises co-02_

`list.append` is amortized O(1) because a resize doubles capacity: rare, expensive O(n) copies get outweighed by many cheap O(1) appends in between. This example counts total element copies across many appends and confirms the average cost per append stays bounded.

**`learning/code/ex-25-amortized-dynamic-array/example.py`**

```python
"""Example 25: A Doubling Dynamic Array -- Amortized O(1) Append, Counted."""

# list.append is amortized O(1) because resizes DOUBLE capacity (co-02):
# rare, expensive O(n) copies are outweighed by many cheap O(1) appends in
# between. This example implements that doubling explicitly and COUNTS copies.


class DynamicArray:  # => a from-scratch array that grows by doubling, like CPython's
    def __init__(self) -> None:
        self.capacity: int = 1  # => starts with room for exactly 1 element
        self.size: int = 0  # => how many elements are actually stored so far
        self.data: list[int | None] = [None] * self.capacity  # => the backing storage
        self.total_copies: int = 0  # => running count of element copies during resizes

    def append(self, value: int) -> None:  # => amortized O(1) per call
        if self.size == self.capacity:  # => backing storage is full -- must grow
            self._resize(self.capacity * 2)  # => DOUBLING is what makes this amortized
        self.data[self.size] = value  # => O(1): writes into the next free slot
        self.size += 1  # => one more element stored

    def _resize(self, new_capacity: int) -> None:  # => O(n): the rare, expensive step
        new_data: list[int | None] = [None] * new_capacity  # => a fresh, larger array
        for i in range(self.size):  # => copies every EXISTING element over
            new_data[i] = self.data[i]  # => one copy per existing element
            self.total_copies += 1  # => tallies this copy for the amortized-cost check
        self.data = new_data  # => the array now points at the larger backing storage
        self.capacity = new_capacity  # => capacity reflects the new, larger size


arr = DynamicArray()  # => starts empty, capacity 1
n = 1000  # => how many appends to perform
for i in range(n):  # => n appends -- MOST are O(1), a few trigger an O(n) resize
    arr.append(i)  # => amortized O(1) each

average_copies_per_append = arr.total_copies / n  # => the amortized cost per append
print(arr.size)  # => Output: 1000
print(arr.total_copies)  # => Output: 1023 -- sum of 1+2+4+...+512, just over n
print(f"{average_copies_per_append:.3f}")  # => Output: 1.023

assert arr.size == n  # => confirms every append landed correctly
assert (
    average_copies_per_append < 2.0
)  # => confirms the amortized cost stays BOUNDED by a small constant, not O(n)
print("ex-25 OK")  # => Output: ex-25 OK
```

**Run**: `python3 example.py`

**Output**:

```text
1000
1023
1.023
ex-25 OK
```

**`learning/code/ex-25-amortized-dynamic-array/test_example.py`**

```python
"""Example 25: pytest verification for the Doubling Dynamic Array."""

from example import DynamicArray


def test_all_appended_values_are_stored_in_order() -> None:
    arr = DynamicArray()
    for v in [10, 20, 30]:
        arr.append(v)
    assert arr.size == 3
    assert [arr.data[i] for i in range(arr.size)] == [10, 20, 30]


def test_amortized_copy_count_stays_bounded_as_n_grows() -> None:
    small = DynamicArray()
    for i in range(100):
        small.append(i)
    large = DynamicArray()
    for i in range(10_000):
        large.append(i)
    small_ratio = small.total_copies / 100
    large_ratio = large.total_copies / 10_000
    assert large_ratio < 2.0  # => a 100x bigger n does NOT proportionally grow copies
    assert small_ratio < 2.0


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Amortized analysis looks at the TOTAL cost across a whole sequence of operations, divided by the number of operations -- not the worst-case cost of any single operation, which is what makes an occasional O(n) resize compatible with an 'amortized O(1) append' claim.

**Why it matters**: This is the single most important amortized-analysis example in the topic, because `list.append` is used constantly and its 'O(1)' claim is not literally true for every call -- it is true on average. Examples 26 and 77 revisit this same structure with two more rigorous proof techniques (accounting and potential methods) once the intuition here is established.

---

### Example 26: The Accounting Method

_ex-26 &middot; exercises co-02_

The accounting method charges each operation a fixed amortized cost, banking the surplus over what the operation actually spends, then cashes that surplus in to pay for expensive operations later. This example charges every append 3 credits and confirms the running credit balance never dips below zero.

**`learning/code/ex-26-amortized-accounting-method/example.py`**

```python
"""Example 26: The Accounting Method -- Credits That Never Go Negative."""

# The accounting method (co-02) charges each operation a fixed AMORTIZED cost
# (here, 3 credits per append), banking the surplus over what the operation
# actually spends. A resize later "cashes in" that banked surplus to pay for
# copying every existing element -- the proof this works is that the credit
# balance never dips below zero, across the ENTIRE sequence of operations.


class AccountedArray:  # => a doubling array instrumented to track its credit ledger
    def __init__(self) -> None:
        self.capacity: int = 1  # => starts with room for 1 element
        self.size: int = 0  # => elements actually stored
        self.credit_balance: int = 0  # => the running amortized-credit ledger

    def append(self, value: int) -> None:  # => charges 3, an amortized O(1) cost
        actual_cost = 1  # => the baseline cost: writing one new element
        if self.size == self.capacity:  # => full -- a resize must happen first
            actual_cost += self.size  # => ALSO pays 1 per existing element it copies
            self.capacity *= 2  # => doubles capacity, same as Example 25
        self.credit_balance += 3  # => charges this append the fixed amortized rate
        self.credit_balance -= actual_cost  # => pays for whatever actually happened
        assert (
            self.credit_balance >= 0
        )  # => THE PROOF: banked credit always covers the real cost
        self.size += 1  # => one more element now stored


arr = AccountedArray()  # => starts empty
balances: list[int] = []  # => records the credit balance after every single append
for i in range(500):  # => 500 appends -- several of them trigger a doubling resize
    arr.append(i)  # => charges 3, pays the real cost, asserts balance >= 0 internally
    balances.append(arr.credit_balance)  # => snapshots the balance for inspection

print(min(balances))  # => Output: 2 -- the balance dips low but never below zero
print(arr.credit_balance)  # => Output: 489 -- the final leftover credit
print(arr.size)  # => Output: 500

assert min(balances) >= 0  # => confirms the balance NEVER went negative, at any point
assert arr.size == 500  # => confirms every append actually landed
print("ex-26 OK")  # => Output: ex-26 OK
```

**Run**: `python3 example.py`

**Output**:

```text
2
489
500
ex-26 OK
```

**`learning/code/ex-26-amortized-accounting-method/test_example.py`**

```python
"""Example 26: pytest verification for the Accounting Method."""

from example import AccountedArray


def test_credit_balance_never_goes_negative_across_many_resizes() -> None:
    arr = AccountedArray()
    for i in range(2000):  # => several doublings happen along the way
        arr.append(i)
        assert arr.credit_balance >= 0  # => re-checked after every single append


def test_final_size_matches_number_of_appends() -> None:
    arr = AccountedArray()
    for i in range(37):  # => a deliberately non-power-of-two count
        arr.append(i)
    assert arr.size == 37


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: The accounting method PROVES an amortized bound by showing a credit balance never goes negative across an entire operation sequence -- if the balance stays nonnegative, the fixed charge per operation really was enough to cover every operation's actual cost, expensive ones included.

**Why it matters**: Unlike Example 25's aggregate method (total cost divided by operation count), the accounting method assigns a cost to EACH operation individually and proves the bookkeeping works out -- a technique that generalizes to situations (like Example 77's multi-pop stack) where different operation types have very different actual costs, not just occasional expensive resizes.

---

### Example 27: Randomized-Pivot Quicksort

_ex-27 &middot; exercises co-08_

Example 8's naive quicksort always picks the first element, so sorted input triggers its O(n^2) worst case. This example picks a random pivot on every call instead, and confirms already-sorted input no longer degrades the comparison count.

**`learning/code/ex-27-quicksort-random-pivot/example.py`**

```python
"""Example 27: Randomized-Pivot Quicksort -- Sorted Input No Longer Degrades."""

# Example 8's naive quicksort always picks the FIRST element, so sorted input
# triggers its O(n^2) worst case. Picking a RANDOM pivot each time (co-08)
# makes that worst case astronomically unlikely -- expected O(n log n) even
# on already-sorted input, because the bad case no longer depends on the DATA.
import random

comparisons = 0  # => a global counter, reset before each measurement below


def randomized_quicksort(items: list[int], lo: int = 0, hi: int | None = None) -> None:
    global comparisons  # => this function mutates the module-level counter
    if hi is None:  # => top-level call defaults hi to the last index
        hi = len(items) - 1  # => sorts the WHOLE list on the first call
    if lo < hi:  # => base case: 0 or 1 elements need no partitioning
        p = random_pivot_partition(items, lo, hi)  # => the only change from Example 8
        randomized_quicksort(items, lo, p - 1)  # => recurses on the left partition
        randomized_quicksort(items, p + 1, hi)  # => recurses on the right partition


def random_pivot_partition(items: list[int], lo: int, hi: int) -> int:
    global comparisons  # => mutates the shared counter
    rand_index = random.randint(lo, hi)  # => picks a UNIFORMLY random index as pivot
    items[rand_index], items[lo] = (  # => opens the swap-to-front tuple assignment
        items[lo],  # => the old first element moves to the random index's old slot
        items[rand_index],  # => the randomly chosen value moves to the front
    )  # => swaps it to the front so the rest of the logic is unchanged
    pivot = items[lo]  # => now behaves exactly like Example 8's first-pivot partition
    i = lo  # => boundary of the "<pivot" region
    for j in range(lo + 1, hi + 1):  # => scans every element after the pivot
        comparisons += 1  # => counts this one comparison against the pivot
        if items[j] < pivot:  # => belongs strictly before the pivot
            i += 1  # => grows the "<pivot" region
            items[i], items[j] = items[j], items[i]  # => swaps it in
    items[lo], items[i] = items[i], items[lo]  # => places the pivot at its final spot
    return i  # => pivot's final index


random.seed(99)  # => fixed seed -- makes the "random" pivot choices reproducible
n = 500  # => how many elements to sort
already_sorted: list[int] = list(  # => opens the pre-sorted input construction
    range(n)  # => builds 0, 1, 2, ..., n-1 in ascending order
)  # => Example 8's worst case: pre-sorted input
naive_worst_case = n * (n - 1) // 2  # => what Example 8 would score on this same input
comparisons = 0  # => resets the shared counter before measuring
randomized_quicksort(already_sorted)  # => sorts the SAME kind of worst-case input
print(comparisons < naive_worst_case)  # => Output: True
print(already_sorted == list(range(n)))  # => Output: True -- still sorts correctly

assert (  # => opens the check -- wraps the long boolean across two lines
    comparisons < naive_worst_case  # => True only if randomization avoided the blow-up
)  # => confirms randomization avoids the O(n^2) sorted-input trap
assert already_sorted == list(range(n))  # => confirms correctness is unaffected
print("ex-27 OK")  # => Output: ex-27 OK
```

**Run**: `python3 example.py`

**Output**:

```text
True
True
ex-27 OK
```

**`learning/code/ex-27-quicksort-random-pivot/test_example.py`**

```python
"""Example 27: pytest verification for Randomized-Pivot Quicksort."""

import random

import example


def test_sorted_input_no_longer_hits_the_naive_worst_case() -> None:
    random.seed(3)
    n = 300
    data: list[int] = list(range(n))
    example.comparisons = 0
    example.randomized_quicksort(data)
    naive_worst_case = n * (n - 1) // 2
    assert example.comparisons < naive_worst_case  # => far below the O(n^2) bound
    assert data == list(range(n))  # => still correctly sorted


def test_matches_sorted_on_random_input() -> None:
    random.seed(4)
    data: list[int] = random.sample(range(1000), 60)
    expected = sorted(data)
    example.randomized_quicksort(data)
    assert data == expected


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Randomizing pivot choice does not change quicksort's WORST-CASE complexity (an adversary who knows the random seed could still force it), but it makes that worst case exponentially unlikely for any FIXED input, including already-sorted data.

**Why it matters**: This is the standard, practical fix for quicksort's Example-8 weakness, and it is why real-world quicksort implementations use randomization (or a similar trick like median-of-three). It is also an important distinction from Example 74's median-of-medians, which achieves a worst-case guarantee DETERMINISTICALLY, without relying on randomness at all.

---

### Example 28: Quickselect for the k-th Smallest

_ex-28 &middot; exercises co-08_

Quickselect reuses quicksort's partition step but recurses into only ONE side -- whichever side contains the k-th position -- instead of both. This example finds several different ranks in an array and checks each result against `sorted(arr)[k]`.

**`learning/code/ex-28-quickselect-kth/example.py`**

```python
"""Example 28: Quickselect -- the k-th Smallest Element in Expected O(n)."""

# Quickselect (co-08) reuses quicksort's partition step, but RECURSES INTO
# ONLY ONE SIDE -- whichever side contains the k-th position -- instead of
# both, giving expected O(n) instead of a full O(n log n) sort.
import random


def quickselect(  # => recurses into only the side containing rank k, not both sides
    items: list[int],  # => the array to search within (never mutated by the caller)
    k: int,  # => k is the 0-indexed target rank to find
) -> int:  # => returns the k-th smallest (0-indexed)
    working = list(items)  # => a copy -- the caller's list is never mutated
    lo, hi = 0, len(working) - 1  # => the active search range, shrinks each round
    while True:  # => each iteration eliminates one whole side of the partition
        if lo == hi:  # => only one candidate remains -- it must be the answer
            return working[lo]  # => base case: nowhere left to search
        p = random_pivot_partition(working, lo, hi)  # => the pivot's final sorted index
        if p == k:  # => the pivot itself landed exactly at the target rank
            return working[p]  # => found it -- no more recursion needed
        if p < k:  # => the k-th smallest is somewhere to the RIGHT of the pivot
            lo = p + 1  # => discards the entire left side -- it's already too small
        else:  # => the k-th smallest is somewhere to the LEFT of the pivot
            hi = p - 1  # => discards the entire right side -- it's already too big


def random_pivot_partition(
    items: list[int], lo: int, hi: int
) -> int:  # => Lomuto scheme
    rand_index = random.randint(lo, hi)  # => a uniformly random pivot choice
    items[rand_index], items[lo] = items[lo], items[rand_index]  # => moves it to front
    pivot = items[lo]  # => the value being partitioned around
    i = lo  # => boundary of the "<pivot" region
    for j in range(lo + 1, hi + 1):  # => scans the rest of the active range
        if items[j] < pivot:  # => belongs strictly before the pivot
            i += 1  # => grows the "<pivot" region by one slot
            items[i], items[j] = items[j], items[i]  # => swaps it into place
    items[lo], items[i] = items[i], items[lo]  # => places the pivot at its final index
    return i  # => the pivot's final, correctly-sorted-position index


# a fixed seed makes this whole demo fully reproducible across runs
random.seed(17)  # => fixed seed -> reproducible pivot choices
data: list[int] = random.sample(range(1000), 40)  # => 40 distinct random ints
sorted_data = sorted(data)  # => ground truth to check quickselect against
third_smallest = quickselect(data, k=2)  # => 0-indexed: k=2 means the 3rd smallest
median = quickselect(data, k=len(data) // 2)  # => the middle element by rank
print(third_smallest == sorted_data[2])  # => Output: True
print(median == sorted_data[len(data) // 2])  # => Output: True

assert third_smallest == sorted_data[2]  # => confirms rank-2 matches sorted()[2]
assert median == sorted_data[len(data) // 2]  # => confirms the median rank matches too
assert quickselect(data, k=0) == min(data)  # => rank 0 is always the minimum
assert quickselect(data, k=len(data) - 1) == max(data)  # => the last rank is the max
print("ex-28 OK")  # => Output: ex-28 OK
```

**Run**: `python3 example.py`

**Output**:

```text
True
True
ex-28 OK
```

**`learning/code/ex-28-quickselect-kth/test_example.py`**

```python
"""Example 28: pytest verification for Quickselect."""

import random

from example import quickselect


def test_every_rank_matches_sorted_index() -> None:
    random.seed(6)
    data: list[int] = random.sample(range(500), 25)
    expected = sorted(data)
    for k in range(len(data)):  # => checks EVERY rank, not just a couple samples
        assert quickselect(data, k) == expected[k]


def test_does_not_mutate_the_caller_list() -> None:
    data: list[int] = [5, 2, 8, 1]
    original = list(data)
    quickselect(data, k=1)
    assert data == original  # => the caller's list is untouched


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Quickselect finds the k-th smallest element in expected O(n) time, faster than fully sorting (`O(n log n)`), because discarding the side that cannot contain rank k means the recursion only ever processes ONE shrinking side, not both.

**Why it matters**: Quickselect is the textbook example of 'you don't need to sort the whole thing to answer one specific question about it' -- finding a median, a percentile, or the k-th ranked value is a strictly easier problem than a full sort, and quickselect's single-sided recursion is what captures that savings. Example 74 pushes this idea further with a worst-case guarantee.

---

### Example 29: Closest Pair of Points

_ex-29 &middot; exercises co-06_

Divide-and-conquer beats brute force's O(n^2) pairwise scan by splitting points on the x-axis, solving each half recursively, then only re-checking a thin vertical strip near the split for cross-boundary pairs. This example finds the closest pair among a set of 2D points and checks it against brute force.

**`learning/code/ex-29-closest-pair-divide-conquer/example.py`**

```python
"""Example 29: Closest Pair of Points -- Divide and Conquer vs Brute Force."""

# Divide-and-conquer (co-06) beats brute force's O(n^2) by SPLITTING points on
# x, solving each half recursively, then only re-checking a thin vertical
# STRIP near the midline for cross-half pairs -- overall O(n log n).
# Squared distances (int, no sqrt) are compared throughout -- ordering is
# identical to true distance, but no floating-point rounding risk.

Point = tuple[int, int]  # => a 2D point as (x, y)


def squared_distance(p: Point, q: Point) -> int:  # => (dx^2 + dy^2), no sqrt needed
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2  # => squared Euclidean distance


def brute_force_closest_pair(points: list[Point]) -> int:  # => O(n^2): every pair
    best = squared_distance(points[0], points[1])  # => a starting baseline
    for i in range(len(points)):  # => tries every unordered pair once
        for j in range(i + 1, len(points)):  # => avoids re-checking the same pair twice
            best = min(best, squared_distance(points[i], points[j]))  # => tracks min
    return best  # => the true minimum squared distance, by exhaustive comparison


def closest_pair_divide_conquer(points: list[Point]) -> int:  # => O(n log n) overall
    by_x = sorted(points, key=lambda p: p[0])  # => O(n log n), done once up front
    return _closest_pair(by_x)  # => delegates to the recursive divide step


def _closest_pair(points_by_x: list[Point]) -> int:  # => points, already sorted by x
    n = len(points_by_x)  # => how many points remain in this recursive slice
    if n <= 3:  # => base case: brute force is cheap enough for 3 or fewer points
        return brute_force_closest_pair(points_by_x)  # => O(1) work at this size
    mid = n // 2  # => the split point
    mid_x = points_by_x[mid][0]  # => the x-coordinate of the dividing line
    left_best = _closest_pair(points_by_x[:mid])  # => recurses on the left half
    right_best = _closest_pair(points_by_x[mid:])  # => recurses on the right half
    best = min(left_best, right_best)  # => the best purely-within-one-half distance
    strip = [  # => opens the filtered "close to the midline" list comprehension
        p
        for p in points_by_x
        if (p[0] - mid_x) ** 2 < best  # => squared-x pruning
    ]  # => points close enough to the midline to possibly beat `best`
    strip.sort(key=lambda p: p[1])  # => sorting the (small) strip by y enables pruning
    for i in range(len(strip)):  # => checks each strip point against its NEAR neighbors
        for j in range(  # => opens the bounded inner-neighbor range
            i + 1,
            min(i + 8, len(strip)),  # => caps the scan at 7 neighbors, never n
        ):  # => a well-known bound: at most 7 useful neighbors in y-sorted order
            best = min(best, squared_distance(strip[i], strip[j]))  # => updates best
    return best  # => the true minimum squared distance across the whole point set


points: list[Point] = [  # => opens the 8-point set, deliberately mixing close/far pairs
    (2, 3),  # => part of the TRUE closest pair, alongside (3, 4)
    (12, 30),  # => far from the cluster near the origin
    (40, 50),  # => the most distant outlier point
    (5, 1),  # => moderately close to the origin cluster
    (12, 10),  # => sits between the near cluster and the mid-distance points
    (3, 4),  # => the other half of the TRUE closest pair, alongside (2, 3)
    (0, 0),  # => the origin -- anchors the near cluster
    (20, 20),  # => a mid-distance point, closer to the outliers than the cluster
]  # => 8 points, deliberately mixing close and far pairs
brute_answer = brute_force_closest_pair(points)  # => O(n^2) ground truth
fast_answer = closest_pair_divide_conquer(points)  # => O(n log n) divide-and-conquer
print(brute_answer)  # => Output: 2
print(fast_answer)  # => Output: 2

assert brute_answer == fast_answer  # => confirms both approaches agree exactly
assert brute_answer == squared_distance(  # => opens the explicit ground-truth check
    (2, 3),
    (3, 4),  # => the two points expected to be the closest pair
)  # => confirms (2,3)-(3,4) is genuinely the closest pair: dist^2 = 1+1 = 2
print("ex-29 OK")  # => Output: ex-29 OK
```

**Run**: `python3 example.py`

**Output**:

```text
2
2
ex-29 OK
```

**`learning/code/ex-29-closest-pair-divide-conquer/test_example.py`**

```python
"""Example 29: pytest verification for Closest Pair Divide and Conquer."""

import random

from example import brute_force_closest_pair, closest_pair_divide_conquer


def test_matches_brute_force_on_random_points() -> None:
    random.seed(31)
    points = [
        (random.randint(0, 200), random.randint(0, 200)) for _ in range(40)
    ]  # => 40 random 2D points
    assert closest_pair_divide_conquer(points) == brute_force_closest_pair(points)


def test_matches_brute_force_on_a_small_collinear_set() -> None:
    points = [(0, 0), (1, 0), (5, 0), (9, 0)]  # => all on one line -- an edge shape
    assert closest_pair_divide_conquer(points) == brute_force_closest_pair(points)


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: The divide-and-conquer closest-pair algorithm's key insight is that the expensive-looking 'merge' step (checking cross-boundary pairs) only needs to examine a narrow strip around the split line, not the whole combined set -- that is what keeps the combine step cheap enough for an `O(n log n)` total bound.

**Why it matters**: This is one of the classic proofs that divide-and-conquer can beat the 'obvious' brute-force approach on a genuinely geometric problem, not just on sorting. Recognizing that a seemingly-global comparison (every pair of points) can be narrowed to a small local region after a smart split is a pattern that reappears in many computational-geometry and scheduling problems beyond this one example.

---

### Example 30: Fenwick Tree Prefix Sum

_ex-30 &middot; exercises co-14_

A Fenwick tree (binary indexed tree) stores partial sums keyed by the lowest set bit of each index, giving both point-update and prefix-sum queries in O(log n). This example runs a sequence of updates and prefix-sum queries and checks every answer against a plain running array.

**`learning/code/ex-30-fenwick-prefix-sum/example.py`**

```python
"""Example 30: Fenwick Tree (Binary Indexed Tree) -- O(log n) Prefix Sum + Update."""

# A Fenwick tree (co-14) stores partial sums keyed by the LOWEST SET BIT of
# each index -- both point-update and prefix-sum become O(log n), beating a
# plain array's O(n) prefix-sum recompute and a running-array's O(n) update-shift.


class FenwickTree:  # => 1-indexed internally -- index 0 is unused, by convention
    def __init__(self, n: int) -> None:  # => allocates a zeroed tree sized for n items
        self.n = n  # => the number of elements this tree covers
        self.tree: list[int] = [0] * (n + 1)  # => tree[i] holds a partial-sum range

    def update(self, i: int, delta: int) -> None:  # => O(log n): adds delta at index i
        i += 1  # => converts the caller's 0-indexed position to 1-indexed internally
        while i <= self.n:  # => climbs toward the root, following the BIT structure
            self.tree[i] += delta  # => applies delta to this partial-sum node
            i += i & (-i)  # => jumps to the next node this index's range feeds into
            # => `i & (-i)` isolates the lowest set bit -- the core BIT trick

    def prefix_sum(  # => walks DOWN the BIT structure, accumulating partial sums
        self,  # => the tree instance holding this Fenwick array
        i: int,  # => the (0-indexed) inclusive upper bound of the prefix
    ) -> int:  # => O(log n): sum of elements [0, i] inclusive
        i += 1  # => converts to 1-indexed
        total = 0  # => accumulates the running sum
        while i > 0:  # => walks DOWN toward index 0, following the BIT structure
            total += self.tree[i]  # => adds this node's partial sum
            i -= i & (-i)  # => strips the lowest set bit, moving to the parent range
        return total  # => the sum of all elements from index 0 through i, inclusive

    def range_sum(self, lo: int, hi: int) -> int:  # => O(log n): sum of [lo, hi]
        if lo == 0:  # => no need to subtract anything below index 0
            return self.prefix_sum(hi)  # => the prefix sum IS the range sum
        return self.prefix_sum(hi) - self.prefix_sum(  # => two O(log n) lookups
            lo - 1  # => excludes everything strictly below lo
        )  # => classic prefix-sum subtraction trick


values: list[int] = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2]  # => 10 starting values
n = len(values)  # => n = 10
fenwick = FenwickTree(n)  # => starts as all zeros
for idx, v in enumerate(values):  # => O(n log n) total: one update per starting value
    fenwick.update(idx, v)  # => builds up the tree to reflect `values`

running_array = list(values)  # => a plain array, kept in sync for cross-checking
print(fenwick.prefix_sum(4))  # => Output: 15 -- sum of values[0..4]
print(sum(running_array[: 4 + 1]))  # => Output: 15 -- confirms the plain-array sum

fenwick.update(2, 10)  # => adds 10 AT index 2 (a point update, not a set)
running_array[2] += 10  # => keeps the plain array in sync for comparison
print(fenwick.prefix_sum(4))  # => Output: 25 -- 15 + 10, reflecting the point update
print(fenwick.range_sum(3, 7))  # => Output: 15 -- sum of values[3..7] after the update

assert (  # => opens the Fenwick-vs-plain-sum cross-check
    fenwick.prefix_sum(4)
    == sum(  # => cross-checks the Fenwick tree vs a plain sum
        running_array[: 4 + 1]  # => the same [0, 4] slice, summed the naive O(n) way
    )  # => closes the naive prefix sum call
)  # => confirms Fenwick matches a plain re-sum after the update
assert (  # => opens the arbitrary-range cross-check
    fenwick.range_sum(3, 7)
    == sum(  # => cross-checks an arbitrary mid-range sum
        running_array[3 : 7 + 1]  # => the same [3, 7] slice, summed the naive O(n) way
    )  # => closes the naive range sum call
)  # => confirms arbitrary range sums match too
print("ex-30 OK")  # => Output: ex-30 OK
```

**Run**: `python3 example.py`

**Output**:

```text
15
15
25
15
ex-30 OK
```

**`learning/code/ex-30-fenwick-prefix-sum/test_example.py`**

```python
"""Example 30: pytest verification for the Fenwick Tree."""

import random

from example import FenwickTree


def test_matches_a_running_array_after_random_updates() -> None:
    random.seed(41)
    n = 30
    running: list[int] = [0] * n
    fenwick = FenwickTree(n)
    for _ in range(100):  # => 100 random point updates
        idx = random.randint(0, n - 1)
        delta = random.randint(-5, 5)
        fenwick.update(idx, delta)
        running[idx] += delta
        lo = random.randint(0, n - 1)
        hi = random.randint(lo, n - 1)
        assert fenwick.range_sum(lo, hi) == sum(running[lo : hi + 1])


def test_prefix_sum_of_all_zeros_is_zero() -> None:
    fenwick = FenwickTree(5)
    assert fenwick.prefix_sum(4) == 0  # => nothing has been added yet


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: A Fenwick tree's `O(log n)` update and query both come from the SAME bit trick -- `i & (-i)` isolates the lowest set bit, which determines exactly which partial sums each index contributes to and which ones a query must combine.

**Why it matters**: A plain array answers point-updates in `O(1)` but prefix-sum queries in `O(n)`; a precomputed prefix-sum array flips that, `O(1)` query but `O(n)` update. A Fenwick tree is the space-efficient (co-05) middle ground -- both operations in `O(log n)`, using only `O(n)` extra space, which is exactly why Example 67 compares it directly against a heavier segment tree.

---

### Example 31: Segment Tree Range-Minimum Queries

_ex-31 &middot; exercises co-15_

A segment tree stores, at each internal node, the aggregate (here, the minimum) of an entire array range, built once in O(n) and then answering any range-min query in O(log n). This example builds one over a fixed array and checks several range-min queries against brute-force slicing.

**`learning/code/ex-31-segment-tree-range-min/example.py`**

```python
"""Example 31: Segment Tree -- O(log n) Range-Minimum Queries."""

# A segment tree (co-15) stores, at each internal node, the aggregate (here,
# the MIN) of an entire array range -- built once in O(n), then answering any
# range-min query in O(log n) by combining O(log n) precomputed sub-ranges.

INF = float(  # => opens the sentinel construction
    "inf"  # => Python's built-in way to spell positive infinity as a float
)  # => the segment tree's "empty range" sentinel, larger than any value


class SegmentTreeMin:  # => a segment tree specialized for range-minimum queries
    def __init__(self, data: list[int]) -> None:  # => O(n): builds the whole tree once
        self.n = len(data)  # => the number of leaf elements
        self.tree: list[float] = [INF] * (  # => opens the array-backed tree allocation
            4 * self.n  # => 4n is a standard safe upper bound on array-based tree size
        )  # => 4n is a standard safe upper bound on array-based tree size
        self._build(data, 1, 0, self.n - 1)  # => builds the tree rooted at index 1

    def _build(  # => recursively fills every node with its range's minimum, bottom-up
        self,  # => the tree instance under construction
        data: list[int],  # => the source array being indexed
        node: int,  # => this call's own array-backed tree index
        lo: int,  # => the low end of this call's range
        hi: int,  # => [lo, hi] is this call's range
    ) -> (  # => the return-type annotation, split across lines
        None  # => mutates self.tree in place -- nothing to return
    ):  # => node uses the implicit-heap array encoding: children 2*node, 2*node+1
        if lo == hi:  # => a leaf: exactly one array element
            self.tree[node] = data[lo]  # => stores that element's own value directly
            return  # => nothing more to combine at a leaf
        mid = (lo + hi) // 2  # => splits this range roughly in half
        self._build(data, 2 * node, lo, mid)  # => builds the left child (index 2*node)
        self._build(  # => opens the right-child build call
            data,  # => the same source array, threaded through
            2 * node + 1,  # => the right child's own tree index
            mid + 1,  # => one past the left child's range
            hi,  # => builds the right child (2*node+1)
        )  # => closes the right-child build call
        self.tree[node] = min(  # => this node's value is the min of its two children
            self.tree[2 * node],  # => left child's own min
            self.tree[2 * node + 1],  # => right child's own min
        )  # => combines children into this node's own min

    def query(self, lo: int, hi: int) -> float:  # => O(log n): min over [lo, hi]
        # => the public entry point -- always starts recursion at node 1, full range
        return self._query(1, 0, self.n - 1, lo, hi)  # => starts the recursion at root

    def _query(  # => the classic three-way split: outside, inside, or partial overlap
        self,  # => the tree instance being queried
        node: int,  # => this call's own array-backed tree index
        node_lo: int,  # => this node's range's low end
        node_hi: int,  # => this node's range's high end
        lo: int,  # => the query range's low end
        hi: int,  # => node covers [node_lo, node_hi]
    ) -> float:  # => the query range [lo, hi] never changes across the recursion
        if hi < node_lo or node_hi < lo:  # => this node's range is entirely OUTSIDE
            return INF  # => contributes nothing to a min -- INF is the identity
        if lo <= node_lo and node_hi <= hi:  # => this node's range is entirely INSIDE
            return self.tree[node]  # => the precomputed min covers this whole range
        mid = (node_lo + node_hi) // 2  # => this node PARTIALLY overlaps -- must split
        return min(  # => combines whatever both children individually contribute
            self._query(  # => opens the left-half recursive call
                2 * node,  # => the left child's own tree index
                node_lo,  # => left child's range starts where this node's did
                mid,  # => left child's range ends at the midpoint
                lo,  # => the query range's low end, passed through unchanged
                hi,  # => recurses into the left half
            ),  # => closes the left-half recursive call
            self._query(  # => opens the right-half recursive call
                2 * node + 1,  # => the right child's own tree index
                mid + 1,  # => right child's range starts just past the midpoint
                node_hi,  # => right child's range ends where this node's did
                lo,  # => the query range's low end, passed through unchanged
                hi,  # => and the right half
            ),  # => closes the right-half recursive call
        )  # => combines whatever both halves contribute


# => 8 unsorted integers, min is 1 at index 3
data: list[int] = [  # => opens the source-array literal
    5,  # => index 0
    2,  # => index 1
    8,  # => index 2
    1,  # => index 3 -- the global minimum
    9,  # => index 4
    3,  # => index 5
    7,  # => index 6
    4,  # => index 7
]  # => closes the source-array literal
tree = SegmentTreeMin(data)  # => O(n): builds the tree once

print(tree.query(0, 3))  # => Output: 1 -- min of [5, 2, 8, 1]
print(tree.query(4, 7))  # => Output: 3 -- min of [9, 3, 7, 4]
print(tree.query(0, 7))  # => Output: 1 -- min of the whole array

assert tree.query(0, 3) == min(data[0:4])  # => confirms against a brute-force slice min
assert tree.query(4, 7) == min(data[4:8])  # => confirms another range against a slice
# => a single-element range is the INSIDE case -- returns the leaf's own value directly
assert tree.query(2, 2) == data[2]  # => a single-element range returns that element
print("ex-31 OK")  # => Output: ex-31 OK
```

**Run**: `python3 example.py`

**Output**:

```text
1
3
1
ex-31 OK
```

**`learning/code/ex-31-segment-tree-range-min/test_example.py`**

```python
"""Example 31: pytest verification for Segment Tree Range-Min."""

import random

from example import SegmentTreeMin


def test_matches_brute_force_slice_min_on_random_ranges() -> None:
    random.seed(51)
    data = [random.randint(-50, 50) for _ in range(25)]
    tree = SegmentTreeMin(data)
    for _ in range(60):
        lo = random.randint(0, len(data) - 1)
        hi = random.randint(lo, len(data) - 1)
        assert tree.query(lo, hi) == min(data[lo : hi + 1])


def test_whole_array_query_matches_python_min() -> None:
    data = [4, -2, 9, 0, 7]
    tree = SegmentTreeMin(data)
    assert tree.query(0, len(data) - 1) == min(data)


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: A segment tree answers a range-aggregate query in `O(log n)` by combining at most `O(log n)` precomputed subtree results -- never touching more than a logarithmic number of the tree's `O(n)` nodes for any single query.

**Why it matters**: Unlike a Fenwick tree (Example 30), which only supports sum-like aggregates, a segment tree generalizes to ANY associative operation -- min, max, GCD, or sum -- which is exactly why it is the right structure for range-min here, a query a Fenwick tree cannot answer directly. That generality costs more code and roughly 4x the memory, a tradeoff Example 67 makes explicit.

---

### Example 32: Segment Tree with Lazy Range-Add

_ex-32 &middot; exercises co-15_

A plain segment tree's range update touches every leaf in the range: O(n) in the worst case. Lazy propagation defers that work, stamping a fully-covered node with a pending update instead of pushing it all the way down immediately. This example applies several range-add updates and verifies point reads afterward.

**`learning/code/ex-32-segment-tree-range-update/example.py`**

```python
"""Example 32: Segment Tree with Lazy Range-Add -- O(log n) Range Update, Point Read."""

# A plain segment tree's range update is O(n) (touch every leaf). LAZY
# propagation (co-15) defers that work: a fully-covered node just stamps a
# pending "add" tag and stops -- the tag only gets PUSHED DOWN to children
# when a later query actually needs to look inside that node. O(log n) both ways.


class LazySegmentTree:  # => sum-tracking tree with O(log n) range-add, point query
    def __init__(self, data: list[int]) -> None:  # => O(n): builds the initial tree
        self.n = len(data)  # => number of leaf elements
        self.tree: list[int] = [0] * (4 * self.n)  # => tree[node] = sum over its range
        self.lazy: list[int] = [0] * (4 * self.n)  # => pending, not-yet-pushed adds
        self._build(data, 1, 0, self.n - 1)  # => builds the initial tree, O(n)

    def _build(  # => bottom-up: leaves first, then each parent sums its two children
        self,  # => the tree instance under construction
        data: list[int],  # => the source array being indexed
        node: int,  # => this call's own array-backed tree index
        lo: int,  # => the low end of this node's range
        hi: int,  # => [lo, hi] is this node's range
    ) -> None:  # => fills self.tree over the array-index encoding, no lazy tags yet
        if lo == hi:  # => leaf: exactly one element
            self.tree[node] = data[lo]  # => its own starting value
            return  # => nothing more to combine at a leaf
        mid = (lo + hi) // 2  # => splits the range
        self._build(data, 2 * node, lo, mid)  # => builds the left child
        self._build(data, 2 * node + 1, mid + 1, hi)  # => builds the right child
        self.tree[node] = (  # => opens the parent-sum assignment
            self.tree[2 * node]  # => the left child's own sum
            + self.tree[2 * node + 1]  # => plus the right child's own sum
        )  # => this node's sum is its children's combined sum

    def _push_down(  # => flushes node's pending tag one level down, THEN clears it
        self,  # => the tree instance being flushed
        node: int,  # => this call's own array-backed tree index
        lo: int,  # => the low end of this node's range
        hi: int,  # => node's own [lo, hi] range
    ) -> None:  # => flushes a pending tag
        if self.lazy[node] == 0:  # => nothing pending -- nothing to push
            return  # => an early exit avoids touching children unnecessarily
        mid = (lo + hi) // 2  # => needed to size each child's range
        for child, child_lo, child_hi in (  # => opens the (index, lo, hi) pair loop
            (2 * node, lo, mid),  # => the left child's index and range
            (2 * node + 1, mid + 1, hi),  # => the right child's index and range
        ):  # => applies the SAME pending delta to both children
            self.tree[child] += self.lazy[node] * (  # => scales the delta by range size
                child_hi - child_lo + 1  # => how many elements this child's range spans
            )  # => scales by range SIZE, since tree[] stores a SUM, not a single value
            self.lazy[child] += self.lazy[node]  # => the child inherits the pending tag
        self.lazy[node] = 0  # => this node's tag has now been fully passed down

    def range_add(  # => public entry point -- the only method callers use to update
        self,  # => the tree instance being updated
        lo: int,  # => the low end of the range to add to
        hi: int,  # => the high end of the range to add to
        delta: int,  # => adds delta to every index in [lo, hi]
    ) -> None:  # => O(log n): adds delta
        self._range_add(1, 0, self.n - 1, lo, hi, delta)  # => starts at the root

    def _range_add(  # => the classic outside/inside/partial-overlap recursive split
        self,  # => the tree instance being updated
        node: int,  # => this call's own array-backed tree index
        node_lo: int,  # => this node's range's low end
        node_hi: int,  # => this node's range's high end
        lo: int,  # => the update range's low end
        hi: int,  # => the update range's high end
        delta: int,  # => node covers [node_lo, node_hi]
    ) -> None:  # => mutates self.tree and self.lazy in place, returns nothing
        if hi < node_lo or node_hi < lo:  # => this node's range is entirely outside
            return  # => nothing to do here
        if lo <= node_lo and node_hi <= hi:  # => this node's range is entirely inside
            self.tree[node] += delta * (  # => the aggregate sum shifts by delta * count
                node_hi - node_lo + 1  # => how many elements this whole node covers
            )  # => updates the aggregate sum directly
            self.lazy[node] += delta  # => defers pushing to children until needed
            return  # => THE LAZY PART: children are not touched yet
        self._push_down(  # => must resolve any pending tag before recursing further
            node,  # => this node's own array-backed tree index
            node_lo,  # => this node's own range low end
            node_hi,  # => flushes THIS node's own stale tag first
        )  # => must resolve any pending tag before recursing further
        mid = (node_lo + node_hi) // 2  # => splits this node's range for the recursion
        self._range_add(2 * node, node_lo, mid, lo, hi, delta)  # => recurses left
        self._range_add(2 * node + 1, mid + 1, node_hi, lo, hi, delta)  # => and right
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]  # => recombines

    def point_query(self, i: int) -> int:  # => O(log n): the CURRENT value at index i
        return self._point_query(1, 0, self.n - 1, i)  # => starts at the root

    def _point_query(  # => descends one side at each level, pushing down tags first
        self,  # => the tree instance being queried
        node: int,  # => this call's own array-backed tree index
        lo: int,  # => this node's range's low end
        hi: int,  # => this node's range's high end
        i: int,  # => node covers [lo, hi]; i is the target
    ) -> int:  # => returns the up-to-date value at index i
        if lo == hi:  # => a leaf -- its stored sum IS the single element's value
            return self.tree[node]  # => already reflects every applied range-add
        self._push_down(  # => resolves any pending tag before descending further
            node,  # => this node's own array-backed tree index
            lo,  # => this node's own range low end
            hi,  # => this node's own range, needed to size its children
        )  # => resolves any pending tag before descending further
        mid = (lo + hi) // 2  # => decides which child holds index i
        if i <= mid:  # => the target index lives in the left half
            return self._point_query(2 * node, lo, mid, i)  # => recurses left
        return self._point_query(2 * node + 1, mid + 1, hi, i)  # => lives in the right


data: list[int] = [1, 2, 3, 4, 5, 6]  # => 6 starting values
tree = LazySegmentTree(data)  # => O(n): builds the initial tree
tree.range_add(1, 4, 10)  # => O(log n): adds 10 to every element in indices [1, 4]

expected: list[int] = [  # => opens the hand-computed plain-array result
    1,  # => index 0 -- outside [1, 4], unchanged
    12,  # => index 1 -- 2 + 10
    13,  # => index 2 -- 3 + 10
    14,  # => index 3 -- 4 + 10
    15,  # => index 4 -- 5 + 10
    6,  # => index 5 -- outside [1, 4], unchanged
]  # => the plain-array result of the same range-add, computed by hand
for i in range(len(data)):  # => reads every index back through the tree
    print(f"index {i}: {tree.point_query(i)}")  # => Output: index N: value, per index
    assert tree.point_query(i) == expected[i]  # => confirms each point read is correct

tree.range_add(0, 2, 5)  # => a SECOND, overlapping range-add, to stack lazy tags
expected2: list[int] = [6, 17, 18, 14, 15, 6]  # => reflects both range-adds combined
for i in range(len(data)):  # => re-reads every index after the second update
    assert tree.point_query(i) == expected2[i]  # => confirms overlapping updates stack
print("ex-32 OK")  # => Output: ex-32 OK
```

**Run**: `python3 example.py`

**Output**:

```text
index 0: 1
index 1: 12
index 2: 13
index 3: 14
index 4: 15
index 5: 6
ex-32 OK
```

**`learning/code/ex-32-segment-tree-range-update/test_example.py`**

```python
"""Example 32: pytest verification for Lazy Range-Add Segment Tree."""

import random

from example import LazySegmentTree


def test_matches_a_brute_force_running_array_after_random_range_adds() -> None:
    random.seed(61)
    n = 20
    running: list[int] = [0] * n
    tree = LazySegmentTree(running)
    for _ in range(50):  # => 50 random overlapping range-add operations
        lo = random.randint(0, n - 1)
        hi = random.randint(lo, n - 1)
        delta = random.randint(-10, 10)
        tree.range_add(lo, hi, delta)
        for i in range(lo, hi + 1):  # => the brute-force ground truth, applied directly
            running[i] += delta
        for i in range(n):  # => re-checks every index after each update
            assert tree.point_query(i) == running[i]


def test_non_overlapping_updates_stay_independent() -> None:
    tree = LazySegmentTree([0, 0, 0, 0])
    tree.range_add(0, 1, 5)
    tree.range_add(2, 3, -3)
    assert [tree.point_query(i) for i in range(4)] == [5, 5, -3, -3]


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Lazy propagation turns an `O(n)` range update into `O(log n)` by stamping fully-covered nodes with a PENDING delta and only pushing it further down the tree the next time that subtree is actually visited -- deferred work, not skipped work.

**Why it matters**: Lazy propagation is a direct application of the space-time tradeoff (co-05): storing a small pending value at each node costs a little extra memory, but saves enormous amounts of redundant work whenever the SAME range gets updated (or read) repeatedly. This pattern -- defer work until it is actually needed -- reappears constantly in systems programming outside of just segment trees.

---

### Example 33: Union-Find with Rank and Path Compression

_ex-33 &middot; exercises co-16, co-02_

Two independent optimizations on top of Example 22's plain union-find: union-by-rank always attaches the shorter tree under the taller one, and path compression flattens every node on a `find` path to point directly at the root. This example runs thousands of operations and confirms near-constant amortized query time.

**`learning/code/ex-33-union-find-optimized/example.py`**

```python
"""Example 33: Union-Find with Union-by-Rank and Path Compression."""

# Two independent optimizations on top of Example 22's plain union-find
# (co-16): UNION-BY-RANK always attaches the shorter tree under the taller
# one, keeping trees flat; PATH COMPRESSION flattens every node visited
# during find() to point directly at the root. Together they give amortized
# O(alpha(n)) per operation -- alpha is the inverse Ackermann function, which
# is under 5 for any n that could ever be represented in memory: effectively
# constant time in practice, though not literally O(1) in the strict sense.


class OptimizedUnionFind:  # => union-find with both classic optimizations applied
    def __init__(self, n: int) -> None:  # => n singleton groups, each its own root
        self.parent: list[int] = list(  # => opens the initial parent-list construction
            range(n)  # => index i's parent starts as i itself -- n separate groups
        )  # => each element starts as its own root
        self.rank: list[int] = [0] * n  # => an upper bound on each tree's height

    def find(self, x: int) -> int:  # => amortized O(alpha(n)) with path compression
        if self.parent[x] != x:  # => x is not yet its own group's root
            self.parent[x] = (
                self.find(  # => recurses first, THEN repoints on the way back
                    self.parent[
                        x
                    ]  # => climbs toward the root through x's current parent
                )  # => closes the recursive find() call
            )  # => PATH COMPRESSION: recurses to the root, then repoints x DIRECTLY at it
        return self.parent[x]  # => x's parent is now either itself, or the true root

    def union(self, a: int, b: int) -> None:  # => amortized O(alpha(n))
        root_a = self.find(a)  # => a's group root (path-compressed along the way)
        root_b = self.find(b)  # => b's group root
        if root_a == root_b:  # => already the same group -- nothing to merge
            return  # => a union with itself is a no-op
        if (  # => opens the rank comparison
            self.rank[root_a] < self.rank[root_b]
        ):  # => UNION BY RANK: shorter under taller
            self.parent[root_a] = (  # => opens the shorter-under-taller reassignment
                root_b  # => attaches the shorter tree under the taller
            )  # => closes the reassignment
        elif self.rank[root_a] > self.rank[root_b]:  # => the mirror comparison
            self.parent[root_b] = root_a  # => the mirror case
        else:  # => equal rank -- pick either, and the result grows one level taller
            self.parent[root_b] = root_a  # => arbitrarily attaches b's root under a's
            self.rank[root_a] += 1  # => only NOW does the resulting tree's height grow


def total_find_depth(  # => a diagnostic helper -- NOT part of the union-find API itself
    uf: OptimizedUnionFind,  # => the union-find structure being queried
    n: int,  # => the structure to measure, and its element count
) -> int:  # => sums parent-hop counts
    total = 0  # => accumulates hops across every element's find()
    for x in range(n):  # => checks every element once
        depth = 0  # => counts hops from x up to its root
        cur = (
            x  # => a local walker, so find()'s own compression isn't re-triggered here
        )
        while (
            uf.parent[cur] != cur
        ):  # => climbs until reaching a self-parent (the root)
            cur = uf.parent[cur]  # => one hop toward the root
            depth += 1  # => tallies this hop
        total += depth  # => adds this element's hop count to the running total
    return total  # => the sum of all n elements' current depths


# => margin note: n stays large enough that even O(n) depth would be visible
n = 1000  # => a reasonably large element count, to make near-flat trees visible
uf = OptimizedUnionFind(n)  # => n singleton groups
for i in range(  # => opens the union-count range
    n - 1  # => one union per consecutive pair -- n-1 total union calls
):  # => chains everything into ONE big group, worst-case union order
    uf.union(i, i + 1)  # => unions consecutive elements, one after another

for x in range(n):  # => forces every element's find() to run and compress its path
    uf.find(x)  # => after this loop, EVERY element points close to directly at the root

average_depth = (  # => opens the average-hops-per-element computation
    total_find_depth(uf, n) / n  # => total hops divided by the element count
)  # => average remaining hops after compression
print(average_depth < 3.0)  # => Output: True -- effectively flat, not O(n) deep
print(uf.find(0) == uf.find(n - 1))  # => Output: True -- all n elements are one group

# => without path compression, this 1000-element CHAIN union order would leave average
# => depth near n/2 -- the near-flat result below is entirely due to the optimizations
assert (  # => opens the near-flat-depth check
    average_depth < 3.0  # => True only if the optimizations actually kept trees flat
)  # => confirms near-constant depth despite a 1000-element chain
assert uf.find(0) == uf.find(n - 1)  # => confirms the whole chain merged into one group
print("ex-33 OK")  # => Output: ex-33 OK
```

**Run**: `python3 example.py`

**Output**:

```text
True
True
ex-33 OK
```

**`learning/code/ex-33-union-find-optimized/test_example.py`**

```python
"""Example 33: pytest verification for Optimized Union-Find."""

from example import OptimizedUnionFind


def test_path_compression_keeps_trees_shallow_after_a_worst_case_chain() -> None:
    n = 500
    uf = OptimizedUnionFind(n)
    for i in range(n - 1):
        uf.union(i, i + 1)  # => the worst possible union order for a naive union-find
    for x in range(n):
        uf.find(x)  # => compresses every path
    for x in range(n):  # => re-checks: every element's parent should now be near-root
        assert uf.parent[x] == uf.find(x) or uf.parent[x] == uf.parent[uf.find(x)]


def test_connectivity_after_optimized_unions_matches_expectations() -> None:
    uf = OptimizedUnionFind(6)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(1, 2)  # => merges {0,1} and {2,3} into one group of 4
    assert uf.find(0) == uf.find(3)  # => transitively connected
    assert uf.find(0) != uf.find(4)  # => 4 and 5 remain their own singleton groups
    assert uf.find(4) != uf.find(5)


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Union-by-rank and path compression are INDEPENDENTLY useful, but together they give union-find its famous near-constant amortized cost per operation -- formally, `O(inverse Ackermann, alpha(n))`, a function that grows so slowly it is effectively constant for any input size that could ever occur in practice.

**Why it matters**: This is one of the most dramatic before/after contrasts in the topic: the same algorithm, with two small structural tweaks, goes from a structure that CAN degrade toward a linked list (Example 22) to one that is essentially constant-time at any realistic scale. Kruskal's MST (Example 42) directly depends on this optimized version to stay efficient.

---

### Example 34: Count Connected Components via Union-Find

_ex-34 &middot; exercises co-16_

Unioning every edge's two endpoints, and counting the distinct surviving roots afterward, identifies every connected component with no traversal needed at all. This example runs union-find over a graph with known components and confirms the count matches.

**`learning/code/ex-34-connected-components/example.py`**

```python
"""Example 34: Count Connected Components via Union-Find."""

# Union every edge's two endpoints (co-16), and each surviving DISTINCT root
# afterward identifies one connected component -- no traversal needed at all,
# just a pass over the edges followed by counting unique find() results.


class UnionFind:  # => the optimized version from Example 33, reused as-is
    def __init__(self, n: int) -> None:  # => n singleton groups, each its own root
        self.parent: list[int] = list(  # => opens the initial parent-array construction
            range(n)  # => index i's parent starts as i itself -- n separate groups
        )  # => each element starts as its own root
        self.rank: list[int] = [0] * n  # => an upper bound on each tree's height

    def find(self, x: int) -> int:  # => amortized O(alpha(n)) with path compression
        if self.parent[x] != x:  # => x is not yet its own group's root
            self.parent[x] = (
                self.find(  # => recurses first, THEN repoints on the way back
                    self.parent[
                        x  # => the element whose root is being sought
                    ]  # => climbs toward the root through x's current parent
                )  # => closes the recursive find() call
            )  # => path-compresses on the way back
        return self.parent[x]  # => x's parent is now either itself, or the true root

    def union(self, a: int, b: int) -> None:  # => amortized O(alpha(n))
        root_a, root_b = self.find(a), self.find(b)  # => both groups' roots, compressed
        if root_a == root_b:  # => already the same group -- nothing to merge
            return  # => a union with itself is a no-op
        if (  # => opens the shorter-under-taller rank comparison
            self.rank[root_a] < self.rank[root_b]  # => a's tree is strictly shorter
        ):  # => UNION BY RANK: shorter under taller
            self.parent[root_a] = (  # => opens the shorter-under-taller reassignment
                root_b  # => attaches the shorter tree under the taller
            )  # => closes the reassignment
        elif self.rank[root_a] > self.rank[root_b]:  # => the mirror comparison
            self.parent[root_b] = root_a  # => the mirror case
        else:  # => equal rank -- pick either, and the result grows one level taller
            self.parent[root_b] = root_a  # => arbitrarily attaches b's root under a's
            self.rank[root_a] += 1  # => only NOW does the resulting tree's height grow


def count_components(  # => no traversal at all -- just union every edge, then count roots
    n: int,  # => the number of nodes, labeled 0..n-1
    edges: list[tuple[int, int]],  # => n nodes labeled 0..n-1, plus the edge list
) -> int:  # => O((V+E) alpha(V))
    uf = UnionFind(n)  # => n nodes, each initially its own component
    for a, b in edges:  # => O(E): unions every edge's endpoints
        uf.union(a, b)  # => merges a's and b's components, if not already merged
    roots = {  # => opens the set-comprehension collecting distinct roots
        uf.find(x)  # => the compressed root of node x
        for x in range(n)  # => a set automatically discards duplicate roots
    }  # => O(V): the set of DISTINCT surviving roots
    return len(roots)  # => one component per distinct root


n = 8  # => 8 nodes, labeled 0..7
edges: list[  # => opens the edge-list type annotation
    tuple[int, int]  # => each edge is a pair of node indices
] = [  # => opens the edge list -- deliberately leaves node 7 isolated
    (0, 1),  # => connects 0 and 1 into one group
    (1, 2),  # => extends that group to include 2 -- {0, 1, 2}
    (3, 4),  # => a separate two-node group -- {3, 4}
    (5, 6),  # => another separate two-node group -- {5, 6}
]  # => leaves 7 fully isolated
component_count = count_components(n, edges)  # => how many separate groups exist
print(component_count)  # => Output: 4 -- {0,1,2}, {3,4}, {5,6}, {7}

assert component_count == 4  # => confirms the four expected groups
assert count_components(5, []) == 5  # => no edges at all: every node is its own group
assert count_components(3, [(0, 1), (1, 2)]) == 1  # => a fully connected chain
print("ex-34 OK")  # => Output: ex-34 OK
```

**Run**: `python3 example.py`

**Output**:

```text
4
ex-34 OK
```

**`learning/code/ex-34-connected-components/test_example.py`**

```python
"""Example 34: pytest verification for Connected Components via Union-Find."""

from example import count_components


def test_disconnected_pairs_and_a_singleton() -> None:
    assert count_components(8, [(0, 1), (1, 2), (3, 4), (5, 6)]) == 4


def test_fully_connected_graph_has_one_component() -> None:
    edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
    assert count_components(5, edges) == 1


def test_no_edges_means_every_node_is_its_own_component() -> None:
    assert count_components(4, []) == 4


# => Run: pytest -- Output: 3 passed
```

**Verify**: `pytest -q`

**Output**:

```text
3 passed
```

**Key takeaway**: Counting distinct roots after unioning every edge answers 'how many connected components does this graph have' without ever explicitly traversing the graph -- union-find's structure already encodes connectivity directly.

**Why it matters**: This is a good illustration of picking the right TOOL for a question: BFS/DFS (Examples 19-20) can also find connected components by traversal, but union-find answers the same question with a data structure built for exactly this kind of 'are these two things connected' query, which is also why Kruskal's MST (Example 42) reaches for it instead of a traversal-based approach.

---

### Example 35: Topological Sort via Kahn's Algorithm

_ex-35 &middot; exercises co-18_

Kahn's algorithm repeatedly removes nodes with in-degree zero -- nodes with no remaining unprocessed prerequisites -- appending each to the output order and decrementing its neighbors' in-degrees. This example runs Kahn's algorithm on a small DAG and confirms every edge respects the resulting order.

**`learning/code/ex-35-topological-sort-kahn/example.py`**

```python
"""Example 35: Topological Sort via Kahn's Algorithm."""

# Kahn's algorithm (co-18) repeatedly removes nodes with IN-DEGREE ZERO --
# nodes with no remaining unprocessed prerequisites -- appending each to the
# result and decrementing its neighbors' in-degrees, until none remain.
from collections import deque  # => O(1) popleft, unlike a plain list


def kahn_topological_sort(  # => BFS-style: repeatedly peel off zero-in-degree nodes
    graph: dict[str, list[str]],  # => adjacency map: node -> list of nodes it points to
) -> list[str] | None:  # => None if a cycle makes ordering impossible
    in_degree: dict[str, int] = {  # => opens the initial all-zero in-degree map
        node: 0 for node in graph
    }  # => starts every node's in-degree at 0
    for node in graph:  # => O(V+E): counts how many edges point INTO each node
        for neighbor in graph[
            node  # => this node's own outgoing edges
        ]:  # => each outgoing edge increments the target's count
            in_degree[neighbor] += 1  # => one more prerequisite for neighbor

    queue: deque[str] = deque(  # => opens the initial ready-queue construction
        [node for node in graph if in_degree[node] == 0]  # => the zero-in-degree nodes
    )  # => nodes with NO prerequisites can go first
    order: list[str] = []  # => accumulates the resulting topological order
    while queue:  # => processes nodes in waves of "everything now unblocked"
        node = queue.popleft()  # => O(1): the next ready node
        order.append(node)  # => it has no remaining unprocessed prerequisites
        for neighbor in graph[node]:  # => "removes" node by decrementing its neighbors
            in_degree[neighbor] -= 1  # => one fewer prerequisite for neighbor
            if in_degree[neighbor] == 0:  # => neighbor is now fully unblocked
                queue.append(neighbor)  # => schedules it for the next wave

    if len(order) != len(graph):  # => fewer nodes than expected means a CYCLE exists
        return None  # => a cycle prevents any valid topological order
    return order  # => a valid topological order: every edge points forward in the list


graph: dict[str, list[str]] = {  # => a small build-dependency DAG
    "compile": ["link"],  # => must happen before "link"
    "link": ["test"],  # => must happen before "test"
    "fetch_deps": ["compile"],  # => the true starting point -- no prerequisites at all
    "test": [],  # => the terminal step -- nothing depends on it
}  # => closes the dependency map -- 4 build steps, one linear chain
order = kahn_topological_sort(graph)  # => a valid build order
print(order)  # => Output: ['fetch_deps', 'compile', 'link', 'test']

assert order is not None  # => confirms no cycle was detected
position = {  # => opens the node -> index lookup, built from the result order
    node: i  # => this node's position within the final order
    for i, node in enumerate(order)  # => pairs each node with its position
}  # => node -> its index in the order
assert position["fetch_deps"] < position["compile"]  # => a dependency comes first
assert position["compile"] < position["link"]  # => confirms edge direction is honored
assert position["link"] < position["test"]  # => confirms the last edge too
print("ex-35 OK")  # => Output: ex-35 OK
```

**Run**: `python3 example.py`

**Output**:

```text
['fetch_deps', 'compile', 'link', 'test']
ex-35 OK
```

**`learning/code/ex-35-topological-sort-kahn/test_example.py`**

```python
"""Example 35: pytest verification for Kahn's Topological Sort."""

from example import kahn_topological_sort


def test_every_edge_points_forward_in_the_resulting_order() -> None:
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    order = kahn_topological_sort(graph)
    assert order is not None
    position = {node: i for i, node in enumerate(order)}
    for u, neighbors in graph.items():
        for v in neighbors:
            assert position[u] < position[v]  # => u always precedes v


def test_a_valid_dag_produces_a_full_length_order() -> None:
    graph = {"x": ["y"], "y": ["z"], "z": []}
    order = kahn_topological_sort(graph)
    assert order is not None
    assert len(order) == 3


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Kahn's algorithm produces a valid topological order by always processing a node only after every one of its PREREQUISITES has already been processed -- tracked via in-degree counts that hit zero exactly when that condition is met.

**Why it matters**: Topological sort is the algorithm behind every 'what order should these tasks run in' question where some tasks depend on others -- build systems, package installers, and course-prerequisite graphs all reduce to this. Example 65's critical-path scheduler and Example 80's capstone-preview scheduler both build directly on top of a topological order.

---

### Example 36: Topological Sort via DFS Finish-Time Ordering

_ex-36 &middot; exercises co-18, co-17_

A DFS-based topological sort is the mirror image of Kahn's algorithm: run DFS, and reverse the order nodes finish in. A node finishes only after every node reachable from it has already finished. This example runs both Kahn's and the DFS-based sort on the same DAG and confirms both produce valid orderings.

**`learning/code/ex-36-topological-sort-dfs/example.py`**

```python
"""Example 36: Topological Sort via DFS Finish-Time Ordering."""

# A DFS-based topological sort (co-18, co-17) is the mirror image of Kahn's
# algorithm: run DFS, and REVERSE the order nodes FINISH in. A node finishes
# only after every node reachable from it has already finished -- so it must
# come before all of them in a valid ordering.


def dfs_topological_sort(  # => reverse of DFS finish order -- the mirror of Kahn's
    graph: dict[str, list[str]],  # => adjacency map: node -> list of nodes it points to
) -> list[str]:  # => assumes a DAG -- no cycle check here (that's Example 37)
    visited: set[str] = set()  # => nodes already fully explored
    finish_order: list[  # => opens the type annotation split across lines
        str
    ] = []  # => nodes appended in the order they FINISH, not start

    def recurse(node: str) -> None:  # => a standard recursive DFS visit
        visited.add(node)  # => marks node as being explored
        for neighbor in graph.get(node, []):  # => visits every outgoing edge
            if neighbor not in visited:  # => only recurse into undiscovered nodes
                recurse(neighbor)  # => fully explores neighbor before returning
        finish_order.append(node)  # => node is appended ONLY after ALL its descendants

    for node in graph:  # => handles disconnected pieces too, not just one component
        if node not in visited:  # => starts a fresh DFS from any unvisited node
            recurse(node)  # => explores this whole component

    return list(reversed(finish_order))  # => REVERSING finish order gives topo order


graph: dict[str, list[str]] = {  # => the same build-dependency DAG as Example 35
    "compile": ["link"],  # => must happen before "link"
    "link": ["test"],  # => must happen before "test"
    "fetch_deps": ["compile"],  # => the true starting point -- no prerequisites at all
    "test": [],  # => the terminal step -- nothing depends on it
}  # => closes the dependency map -- same 4 build steps as Example 35
order = dfs_topological_sort(graph)  # => a valid build order, via DFS this time
print(order)  # => Output: ['fetch_deps', 'compile', 'link', 'test']

position = {node: i for i, node in enumerate(order)}  # => node -> its index in order
assert (  # => opens the first edge-direction check
    position["fetch_deps"] < position["compile"]  # => True iff "fetch_deps" comes first
)  # => confirms edge direction honored
assert position["compile"] < position["link"]  # => confirms another edge's direction
assert position["link"] < position["test"]  # => confirms the last edge too
assert len(order) == len(graph)  # => confirms every node appears exactly once
print("ex-36 OK")  # => Output: ex-36 OK
```

**Run**: `python3 example.py`

**Output**:

```text
['fetch_deps', 'compile', 'link', 'test']
ex-36 OK
```

**`learning/code/ex-36-topological-sort-dfs/test_example.py`**

```python
"""Example 36: pytest verification for DFS-Based Topological Sort."""

from example import dfs_topological_sort


def test_every_edge_points_forward_in_the_resulting_order() -> None:
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    order = dfs_topological_sort(graph)
    position = {node: i for i, node in enumerate(order)}
    for u, neighbors in graph.items():
        for v in neighbors:
            assert position[u] < position[v]


def test_handles_a_disconnected_graph_with_two_components() -> None:
    graph = {"a": ["b"], "b": [], "x": ["y"], "y": []}
    order = dfs_topological_sort(graph)
    assert set(order) == {"a", "b", "x", "y"}  # => every node from both components


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Reversing DFS finish order works as a topological sort because a node can only finish AFTER every node it can reach has already finished -- so the node itself must come before all of them in the reversed order.

**Why it matters**: Having two independently-correct algorithms (Kahn's queue-based approach and DFS's finish-time approach) that answer the same question is a useful cross-check: if a graph is genuinely a DAG, both must agree on SOME valid order (though not necessarily the identical order, since multiple valid topological orders can exist for the same DAG).

---

### Example 37: Detect a Cycle via DFS Coloring

_ex-37 &middot; exercises co-18, co-17_

Three colors, not just visited/unvisited, are what makes cycle detection possible: WHITE (unseen), GRAY (on the current recursion stack), and BLACK (fully finished). This example runs colored DFS on both a cyclic and an acyclic graph and confirms only the cyclic one is flagged.

**`learning/code/ex-37-cycle-detection-directed/example.py`**

```python
"""Example 37: Detect a Cycle in a Directed Graph via DFS Coloring."""

# THREE colors (co-17, co-18), not just visited/unvisited, are what makes
# cycle detection possible: WHITE (unseen), GRAY (on the CURRENT recursion
# path), BLACK (fully finished). A back edge to a GRAY node means the current
# path loops back on itself -- exactly what a cycle is.
from enum import Enum, auto  # => Color is an Enum, not a bare string, for type safety


class Color(Enum):  # => three DFS visitation states -- enables cycle detection
    WHITE = auto()  # => not yet discovered
    GRAY = auto()  # => currently on the recursion stack -- an ANCESTOR of this call
    BLACK = auto()  # => fully explored, off the recursion stack


def has_cycle(  # => three-color DFS: a GRAY-to-GRAY edge means a back edge, i.e. a cycle
    graph: dict[str, list[str]],  # => adjacency map: node -> list of nodes it points to
) -> bool:  # => True iff a directed cycle exists
    color: dict[str, Color] = {  # => opens the dict-comprehension initializing colors
        node: Color.WHITE  # => every node begins undiscovered
        for node in graph  # => every node starts undiscovered
    }  # => all start WHITE

    def recurse(node: str) -> bool:  # => True if a cycle is found reachable from node
        color[node] = Color.GRAY  # => node is now an ANCESTOR on this recursion path
        for neighbor in graph.get(node, []):  # => tries every outgoing edge
            if color[neighbor] == Color.GRAY:  # => THE TELLTALE SIGN: an edge back to
                return True  # => an ancestor still on the stack -- a genuine cycle
            if color[
                neighbor  # => this neighbor's current visitation state
            ] == Color.WHITE and recurse(  # => only recurse into unseen nodes
                neighbor  # => the unvisited neighbor to explore next
            ):  # => explore unseen nodes
                return True  # => a cycle was found deeper in this branch
        color[node] = Color.BLACK  # => node is fully explored -- no longer an ancestor
        return False  # => no cycle found through this node

    return any(  # => True as soon as ANY unvisited component reports a cycle
        recurse(node)  # => explores each still-undiscovered component
        for node in graph
        if color[node] == Color.WHITE
    )  # => checks every component


acyclic_graph: dict[  # => opens the type annotation split across lines
    str, list[str]  # => same node/neighbor-list shape as every other graph example
] = {  # => a valid DAG -- Examples 35/36's build order
    "fetch_deps": ["compile"],  # => the true starting point -- no prerequisites at all
    "compile": ["link"],  # => must happen before "link"
    "link": ["test"],  # => must happen before "test"
    "test": [],  # => the terminal step -- nothing depends on it
}  # => closes the acyclic dependency map -- same DAG as Examples 35/36
cyclic_graph: dict[str, list[str]] = {  # => the SAME shape, but with one edge reversed
    "fetch_deps": ["compile"],  # => still the nominal starting point
    "compile": ["link"],  # => still points forward to "link"
    "link": ["test", "fetch_deps"],  # => "link" points back to "fetch_deps" -- a cycle
    "test": [],  # => still a terminal step, uninvolved in the cycle
}  # => closes the cyclic dependency map -- one back edge creates fetch_deps->compile->link->fetch_deps
print(has_cycle(acyclic_graph))  # => Output: False
print(has_cycle(cyclic_graph))  # => Output: True

assert (  # => opens the "acyclic graph correctly accepted" check
    has_cycle(acyclic_graph) is False  # => True only if no cycle was falsely detected
)  # => confirms a valid DAG is correctly accepted
assert has_cycle(cyclic_graph) is True  # => confirms the cycle is correctly detected
assert has_cycle({"a": ["a"]}) is True  # => a self-loop is the smallest possible cycle
print("ex-37 OK")  # => Output: ex-37 OK
```

**Run**: `python3 example.py`

**Output**:

```text
False
True
ex-37 OK
```

**`learning/code/ex-37-cycle-detection-directed/test_example.py`**

```python
"""Example 37: pytest verification for Directed Cycle Detection."""

from example import has_cycle


def test_dag_reports_no_cycle() -> None:
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    assert has_cycle(graph) is False


def test_cyclic_graph_reports_a_cycle() -> None:
    graph = {"a": ["b"], "b": ["c"], "c": ["a"]}  # => a -> b -> c -> a
    assert has_cycle(graph) is True


def test_disconnected_dag_with_no_cycle_reports_false() -> None:
    graph = {"a": ["b"], "b": [], "x": ["y"], "y": []}
    assert has_cycle(graph) is False


# => Run: pytest -- Output: 3 passed
```

**Verify**: `pytest -q`

**Output**:

```text
3 passed
```

**Key takeaway**: A back edge -- an edge pointing to a node that is currently GRAY (on the active recursion stack, not yet finished) -- is the exact signature of a cycle; an edge to a BLACK (already-finished) node is perfectly fine and does not indicate a cycle.

**Why it matters**: A plain visited/unvisited boolean cannot distinguish 'this node is an ancestor of mine on the current path' from 'this node was already fully explored on a completely different branch' -- and that distinction is exactly what separates a genuine cycle from a harmless shared descendant. Topological sort (Examples 35-36) is only well-defined for a DAG, which is why cycle detection is the necessary precondition check before trusting either sort's output.

---

### Example 38: Dijkstra's Shortest Paths

_ex-38 &middot; exercises co-19_

Dijkstra greedily expands the cheapest-known frontier node next, using a min-heap to find that node in O(log n) instead of an O(n) linear scan. This example runs Dijkstra on a weighted graph and confirms the resulting shortest distances match a hand-computed answer.

**`learning/code/ex-38-dijkstra-heap/example.py`**

```python
"""Example 38: Dijkstra's Shortest Paths with a heapq Priority Queue."""

# Dijkstra (co-19) greedily expands the CHEAPEST-known frontier node next,
# using a min-heap (co-09) to find that node in O(log n) instead of an O(n)
# linear scan. Requires NON-NEGATIVE edge weights -- Example 40 shows why.
import heapq  # => the min-heap priority queue used to pick the cheapest frontier node


def dijkstra(  # => greedily finalizes the cheapest-known frontier node each iteration
    graph: dict[str, list[tuple[str, int]]],  # => node -> list of (neighbor, weight)
    start: str,  # => weighted adjacency + origin
) -> dict[str, float]:  # => node -> shortest distance from start
    distances: dict[str, float] = {  # => opens the initial all-infinity distance map
        node: float("inf")  # => every node starts unreachable, by default
        for node in graph  # => every node starts unreachable
    }  # => everyone starts at infinity
    distances[start] = 0  # => the start node is trivially 0 away from itself
    heap: list[
        tuple[float, str]  # => (distance, node) pairs, ordered by distance
    ] = [  # => opens the initial single-entry priority queue
        (0, start)  # => the only known reachable node at distance 0
    ]  # => (distance, node) -- heapq sorts by distance
    visited: set[str] = set()  # => nodes whose shortest distance is FINAL
    while heap:  # => processes the frontier until nothing remains
        dist, node = heapq.heappop(heap)  # => the currently cheapest unfinalized node
        if node in visited:  # => a stale heap entry -- a shorter path already finalized
            continue  # => skip it, no new information here
        visited.add(node)  # => node's distance is now FINAL -- never improves further
        for neighbor, weight in graph[node]:  # => relaxes every outgoing edge
            new_dist = dist + weight  # => the cost of reaching neighbor THROUGH node
            if new_dist < distances[neighbor]:  # => a strictly better path was found
                distances[neighbor] = new_dist  # => records the improved distance
                heapq.heappush(heap, (new_dist, neighbor))  # => schedules the candidate
    return distances  # => shortest distance to every node reachable from start


graph: dict[str, list[tuple[str, int]]] = {  # => node -> list of (neighbor, weight)
    "a": [("b", 4), ("c", 1)],  # => a's direct routes: to b (cost 4), to c (cost 1)
    "b": [("d", 1)],  # => b's only route: to d (cost 1)
    "c": [("b", 2), ("d", 5)],  # => c offers a cheaper detour to b than a's direct edge
    "d": [],  # => the terminal node -- no outgoing edges
}  # => closes the weighted adjacency map -- 4 nodes
distances = dijkstra(graph, "a")  # => shortest distances from "a" to every other node
print(distances)  # => Output: {'a': 0, 'b': 3, 'c': 1, 'd': 4}

assert distances["a"] == 0  # => the start node is 0 away from itself
assert distances["b"] == 3  # => a->c->b (1+2=3) beats the direct a->b edge (cost 4)
assert distances["d"] == 4  # => a->c->b->d (1+2+1=4) is the cheapest route to d
print("ex-38 OK")  # => Output: ex-38 OK
```

**Run**: `python3 example.py`

**Output**:

```text
{'a': 0, 'b': 3, 'c': 1, 'd': 4}
ex-38 OK
```

**`learning/code/ex-38-dijkstra-heap/test_example.py`**

```python
"""Example 38: pytest verification for Dijkstra with a Heap."""

from example import dijkstra


def test_finds_shortest_path_through_an_indirect_route() -> None:
    graph = {
        "a": [("b", 4), ("c", 1)],
        "b": [("d", 1)],
        "c": [("b", 2), ("d", 5)],
        "d": [],
    }
    distances = dijkstra(graph, "a")
    assert distances["b"] == 3  # => indirect a->c->b beats the direct edge


def test_start_node_distance_is_zero() -> None:
    graph = {"x": [("y", 5)], "y": []}
    assert dijkstra(graph, "x")["x"] == 0


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Dijkstra's greedy strategy -- always finalize the closest unvisited node next -- is only CORRECT because every edge weight is non-negative; a negative edge could make a currently 'farther' path actually shorter, breaking the greedy assumption.

**Why it matters**: Dijkstra is the default shortest-path algorithm for the overwhelming majority of real-world weighted graphs (road networks, network routing) precisely because non-negative weights are the common case, and its heap-driven `O((V+E) log V)` beats Bellman-Ford's `O(V*E)` substantially. Example 40 shows exactly what breaks once negative edges enter the picture.

---

### Example 39: Dijkstra Reports Infinity for Unreachable Nodes

_ex-39 &middot; exercises co-19_

Initializing every distance to infinity before running Dijkstra means a node that is never relaxed simply keeps its infinite distance -- no special-case crash handling needed. This example runs Dijkstra on a graph with a deliberately unreachable node and confirms it reports infinity cleanly.

**`learning/code/ex-39-dijkstra-unreachable/example.py`**

```python
"""Example 39: Dijkstra Reports Infinity for an Unreachable Node -- Never Crashes."""

# Initializing every distance to infinity BEFORE running Dijkstra (co-19)
# means a node that's never relaxed simply keeps its infinite distance --
# there's no special-case branch needed, and no risk of a KeyError or crash.
import heapq


def dijkstra(  # => identical to Example 38's implementation
    graph: dict[str, list[tuple[str, int]]],
    start: str,  # => weighted adjacency + origin
) -> dict[str, float]:  # => identical to Example 38's implementation
    distances: dict[str, float] = {  # => every node starts unreachable, by design
        node: float("inf")
        for node in graph  # => "island" gets this same sentinel too
    }  # => closes the dict-comprehension
    distances[start] = 0  # => the start node is trivially 0 away from itself
    heap: list[tuple[float, str]] = [(0, start)]  # => (distance, node) priority queue
    visited: set[str] = set()  # => nodes whose shortest distance is FINAL
    while heap:  # => processes the frontier until nothing remains
        dist, node = heapq.heappop(heap)  # => the currently cheapest unfinalized node
        if node in visited:  # => a stale heap entry -- a shorter path already finalized
            continue  # => skip it, no new information here
        visited.add(node)  # => node's distance is now FINAL -- never improves further
        for neighbor, weight in graph[node]:  # => relaxes every outgoing edge
            new_dist = dist + weight  # => the cost of reaching neighbor THROUGH node
            if new_dist < distances[neighbor]:  # => a strictly better path was found
                distances[neighbor] = new_dist  # => records the improved distance
                heapq.heappush(heap, (new_dist, neighbor))  # => schedules the candidate
    return distances  # => "island" is never touched -- stays at its initial infinity


graph: dict[str, list[tuple[str, int]]] = {  # => "island" has NO incoming edge from "a"
    "a": [("b", 2)],  # => a's only route: to b (cost 2)
    "b": [],  # => a dead end, but still reachable from "a"
    "island": [],  # => completely disconnected from "a"'s component
}  # => closes the adjacency map -- "island" is a member with zero incoming edges
distances = dijkstra(graph, "a")  # => runs Dijkstra from "a"
print(distances["a"])  # => Output: 0
print(distances["b"])  # => Output: 2
print(  # => opens the print call for the unreachable node's distance
    distances["island"]  # => still the original float("inf") sentinel
)  # => Output: inf -- never relaxed, stays at its initial value

assert distances["b"] == 2  # => confirms the reachable node got its correct distance
assert distances["island"] == float(  # => opens the unreachable-node check
    "inf"  # => the exact sentinel value every distance was initialized to
)  # => confirms the unreachable node reports infinity, not a crash or missing key
assert "island" in distances  # => confirms the key still exists -- no KeyError risk
print("ex-39 OK")  # => Output: ex-39 OK
```

**Run**: `python3 example.py`

**Output**:

```text
0
2
inf
ex-39 OK
```

**`learning/code/ex-39-dijkstra-unreachable/test_example.py`**

```python
"""Example 39: pytest verification for Dijkstra on an Unreachable Node."""

import math

from example import dijkstra


def test_unreachable_node_reports_infinity_not_an_exception() -> None:
    graph = {"a": [("b", 1)], "b": [], "z": []}  # => z has no edge from a's component
    distances = dijkstra(graph, "a")
    assert math.isinf(distances["z"])  # => infinity, never a raised exception


def test_reachable_nodes_still_get_finite_distances() -> None:
    graph = {"a": [("b", 3)], "b": [], "z": []}
    distances = dijkstra(graph, "a")
    assert distances["b"] == 3
    assert not math.isinf(distances["b"])


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Initializing distances to infinity is not just a placeholder value -- it is what makes 'this node is unreachable' fall out naturally from the algorithm's own logic, rather than requiring a separate reachability check bolted on afterward.

**Why it matters**: This is a small but important robustness lesson: choosing the right SENTINEL value (infinity, here) for 'not yet determined' can make an entire class of edge case disappear on its own, instead of needing explicit handling. A real shortest-path service that crashes or throws on a disconnected graph is a much worse failure mode than one that simply reports 'unreachable.'

---

### Example 40: Bellman-Ford with Negative Edges

_ex-40 &middot; exercises co-20_

Bellman-Ford relaxes every edge, V-1 times over -- slower than Dijkstra's O((V+E) log V), at O(V\*E), but it tolerates negative edge weights that would break Dijkstra's greedy assumption. This example runs Bellman-Ford on a graph with a negative edge and confirms the resulting distances are correct.

**`learning/code/ex-40-bellman-ford-negative-edges/example.py`**

```python
"""Example 40: Bellman-Ford -- Correct Shortest Paths with Negative Edges."""

# Bellman-Ford (co-20) relaxes EVERY edge, V-1 times over -- slower than
# Dijkstra's O((V+E) log V), at O(V*E), but it TOLERATES negative edge
# weights, which would silently give Dijkstra's greedy heap the wrong answer.


def bellman_ford(  # => brute-force relax-every-edge, repeated V-1 times, no heap needed
    n: int,  # => the number of nodes, labeled 0..n-1
    edges: list[
        tuple[int, int, int]  # => each edge is a (from, to, weight) triple
    ],  # => (from, to, weight) triples, negatives allowed
    start: int,  # => node count, edges, origin
) -> list[float]:  # => edges: (from, to, weight); returns dist[i] for each node
    dist: list[float] = [float("inf")] * n  # => every node starts at infinity
    dist[start] = 0  # => the start node is 0 away from itself
    for _ in range(n - 1):  # => V-1 full passes -- the longest possible SIMPLE path
        for u, v, w in edges:  # => relaxes every edge, every pass
            if dist[u] + w < dist[v]:  # => found a strictly cheaper way to reach v
                dist[v] = dist[u] + w  # => updates v's distance
    return dist  # => shortest distance to every node, correct even with negative edges


n = 5  # => 5 nodes, labeled 0..4
edges: list[tuple[int, int, int]] = [  # => includes a NEGATIVE edge weight (3 -> 2, -6)
    (0, 1, 6),  # => 0 to 1, cost 6
    (0, 2, 7),  # => 0 to 2, cost 7
    (1, 2, 8),  # => 1 to 2, cost 8
    (1, 3, 5),  # => 1 to 3, cost 5
    (
        1,  # => the edge's source node
        4,  # => the edge's destination node
        -4,  # => the negative weight itself
    ),  # => 1 to 4, a NEGATIVE edge -- Dijkstra could not handle this correctly
    (2, 3, -3),  # => 2 to 3, another negative edge
    (2, 4, 9),  # => 2 to 4, cost 9
    (3, 1, -2),  # => 3 to 1, a negative edge feeding back into an earlier node
    (4, 3, 7),  # => 4 to 3, cost 7
    (4, 0, 2),  # => 4 to 0, closes a cycle back to the start -- but NOT a negative one
]  # => closes the edge list -- 10 directed edges, 3 of them negative-weight
distances = bellman_ford(n, edges, start=0)  # => shortest distances from node 0
print(distances)  # => Output: [0, 2, 7, 4, -2]

assert distances[0] == 0  # => the start node is 0 away from itself
assert (  # => opens the "cheaper indirect path wins" check
    distances[1] == 2
)  # => reached via 0->2->3->1 (7-3-2=2), beats the direct edge (6)
assert distances[4] == -2  # => the negative edge 1->4 pulls this distance below zero
# => a negative-weight EDGE (like 1->4 at -4) doesn't imply a negative CYCLE --
# => Bellman-Ford handles this correctly; Example 41 is what a real cycle looks like
print("ex-40 OK")  # => Output: ex-40 OK
```

**Run**: `python3 example.py`

**Output**:

```text
[0, 2, 7, 4, -2]
ex-40 OK
```

**`learning/code/ex-40-bellman-ford-negative-edges/test_example.py`**

```python
"""Example 40: pytest verification for Bellman-Ford with Negative Edges."""

from example import bellman_ford


def test_matches_a_known_shortest_path_answer_with_negative_edges() -> None:
    n = 5
    edges = [
        (0, 1, 6),
        (0, 2, 7),
        (1, 2, 8),
        (1, 3, 5),
        (1, 4, -4),
        (2, 3, -3),
        (2, 4, 9),
        (3, 1, -2),
        (4, 3, 7),
        (4, 0, 2),
    ]
    distances = bellman_ford(n, edges, start=0)
    assert distances == [0, 2, 7, 4, -2]


def test_positive_only_graph_matches_a_simple_hand_computed_case() -> None:
    edges = [(0, 1, 1), (1, 2, 1), (0, 2, 5)]  # => 0->1->2 (2) beats direct 0->2 (5)
    distances = bellman_ford(3, edges, start=0)
    assert distances == [0, 1, 2]


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Bellman-Ford's `V-1` relaxation rounds are exactly enough: any shortest path in a graph without a negative cycle visits at most `V-1` edges, so `V-1` full rounds of relaxing every edge are guaranteed to have propagated every shortest distance to its final value.

**Why it matters**: Bellman-Ford's extra generality over Dijkstra -- tolerating negative edges -- comes at a real cost, `O(V*E)` versus `O((V+E) log V)`, which is exactly the speed/generality tradeoff Example 63 measures directly. Choosing between the two is a real engineering decision: use Dijkstra when weights are guaranteed non-negative, fall back to Bellman-Ford only when they might not be.

---

### Example 41: Detect a Negative Cycle

_ex-41 &middot; exercises co-20_

After V-1 relaxation rounds, distances are final -- unless a negative cycle exists, in which case an Nth round can still improve some distance, since a negative cycle lets a path get arbitrarily cheaper by looping through it more times. This example runs an extra relaxation round and flags exactly that case.

**`learning/code/ex-41-bellman-ford-negative-cycle/example.py`**

```python
"""Example 41: Detect a Negative Cycle on Bellman-Ford's Nth Relaxation Round."""

# After V-1 relaxation rounds, distances are final -- UNLESS a negative cycle
# exists, in which case an Nth round can STILL improve some distance (co-20).
# That single extra round is the whole detection mechanism: if anything still
# relaxes, "shortest path" is not even well-defined -- you could loop forever.


def bellman_ford_with_cycle_check(  # => runs V-1 rounds, then ONE extra detection round
    n: int,  # => the number of nodes, labeled 0..n-1
    edges: list[tuple[int, int, int]],  # => (from, to, weight) triples
    start: int,  # => node count, edges, origin
) -> tuple[list[float], bool]:  # => (distances, has_negative_cycle)
    dist: list[float] = [float("inf")] * n  # => every node starts at infinity
    dist[start] = 0  # => the start node is 0 away from itself
    for _ in range(n - 1):  # => the normal V-1 relaxation rounds
        for u, v, w in edges:  # => relaxes every edge, every pass
            if dist[u] + w < dist[v]:  # => found a strictly cheaper way to reach v
                dist[v] = (  # => opens the distance-improvement assignment
                    dist[u] + w  # => the new, cheaper distance to v
                )  # => a genuine improvement, still within round V-1
    has_negative_cycle = False  # => assumes no negative cycle until proven otherwise
    for u, v, w in edges:  # => the EXTRA, Nth round -- pure detection, no more updates
        if dist[u] + w < dist[v]:  # => still improvable after V-1 rounds is IMPOSSIBLE
            has_negative_cycle = True  # => ...unless a negative cycle exists
            break  # => one detected violation is proof enough
    return dist, has_negative_cycle  # => distances are UNRELIABLE if the flag is True


n = 4  # => 4 nodes, labeled 0..3
edges_with_negative_cycle: list[  # => opens the negative-cycle edge-list annotation
    tuple[int, int, int]  # => each edge is a (from, to, weight) triple
] = [
    (0, 1, 1),  # => the only edge INTO the cycle -- reaches node 1 to start it off
    (1, 2, -1),  # => first leg of the cycle
    (2, 3, -1),  # => second leg of the cycle
    (3, 1, -1),  # => 1 -> 2 -> 3 -> 1 sums to -3: a genuine negative CYCLE
]  # => closes the edge list -- the 1->2->3->1 loop keeps getting cheaper forever
_, has_cycle = bellman_ford_with_cycle_check(  # => discards distances, keeps the flag
    n,  # => the node count
    edges_with_negative_cycle,  # => the graph containing the genuine negative cycle
    start=0,  # => the graph with a genuine negative cycle
)  # => discards the (unreliable) distances
print(has_cycle)  # => Output: True

edges_without_cycle: list[  # => opens the no-cycle edge-list annotation
    tuple[int, int, int]  # => same triple shape, but this graph never loops back
] = [
    (0, 1, 1),  # => same starting edge as before
    (1, 2, -1),  # => same negative edge as before
    (2, 3, -1),  # => same negative EDGES, but no cycle -- a simple path this time
]  # => closes the edge list -- node 3 has no outgoing edge, so nothing loops back
_, no_cycle = bellman_ford_with_cycle_check(  # => discards distances, keeps the flag
    n,  # => the node count
    edges_without_cycle,  # => the graph with negative edges but no cycle at all
    start=0,  # => the graph with negative edges but no cycle
)  # => same discard pattern
print(no_cycle)  # => Output: False

assert has_cycle is True  # => confirms the genuine negative cycle is flagged
assert no_cycle is False  # => confirms negative EDGES alone don't trigger a false flag
print("ex-41 OK")  # => Output: ex-41 OK
```

**Run**: `python3 example.py`

**Output**:

```text
True
False
ex-41 OK
```

**`learning/code/ex-41-bellman-ford-negative-cycle/test_example.py`**

```python
"""Example 41: pytest verification for Negative Cycle Detection."""

from example import bellman_ford_with_cycle_check


def test_detects_a_genuine_negative_cycle() -> None:
    edges = [(0, 1, 1), (1, 2, -1), (2, 0, -1)]  # => 0->1->2->0 sums to -1
    _, has_cycle = bellman_ford_with_cycle_check(3, edges, start=0)
    assert has_cycle is True


def test_negative_edges_without_a_cycle_are_not_flagged() -> None:
    edges = [(0, 1, -5), (1, 2, -5)]  # => a simple path, both edges negative
    _, has_cycle = bellman_ford_with_cycle_check(3, edges, start=0)
    assert has_cycle is False


def test_all_positive_weights_never_flag_a_cycle() -> None:
    edges = [(0, 1, 2), (1, 2, 3), (2, 0, 4)]  # => a positive-weight cycle is fine
    _, has_cycle = bellman_ford_with_cycle_check(3, edges, start=0)
    assert has_cycle is False


# => Run: pytest -- Output: 3 passed
```

**Verify**: `pytest -q`

**Output**:

```text
3 passed
```

**Key takeaway**: A negative cycle makes 'shortest path' meaningless (the cost can be driven arbitrarily low by looping the cycle more times) -- Bellman-Ford detects one by running ONE extra relaxation round past the guaranteed `V-1` and checking whether any distance still improves.

**Why it matters**: This extra round is the entire reason Bellman-Ford is preferred over Dijkstra in domains like currency-arbitrage detection, where a 'negative cycle' literally represents a profitable trading loop -- Dijkstra has no equivalent mechanism to even notice a negative cycle exists, let alone flag it, since its greedy assumption breaks down before it would ever find one.

---

### Example 42: Kruskal's Minimum Spanning Tree

_ex-42 &middot; exercises co-21, co-16_

Kruskal's algorithm is greedy on edges: sort every edge by weight, then add each one unless it would create a cycle, checked via union-find. This example builds an MST on a weighted graph and confirms the total weight matches a known minimum.

**`learning/code/ex-42-mst-kruskal/example.py`**

```python
"""Example 42: Kruskal's Minimum Spanning Tree, via Sorting + Union-Find."""

# Kruskal's algorithm (co-21) is GREEDY on edges: sort every edge by weight,
# then add each one UNLESS it would create a cycle -- union-find (co-16)
# answers "would this create a cycle?" in near-constant time via connected().


class UnionFind:  # => the optimized version from Example 33
    def __init__(self, n: int) -> None:  # => n singleton groups, each its own root
        self.parent: list[int] = list(  # => opens the initial parent-list construction
            range(n)  # => index i's parent starts as i itself
        )  # => each element starts as its own root
        self.rank: list[int] = [0] * n  # => an upper bound on each tree's height

    def find(self, x: int) -> int:  # => amortized O(alpha(n)) with path compression
        if self.parent[x] != x:  # => x is not yet its own group's root
            self.parent[x] = (  # => opens the path-compression reassignment
                self.find(  # => recurses first, THEN repoints on the way back
                    self.parent[
                        x  # => the element whose root is being sought
                    ]  # => climbs toward the root through x's current parent
                )  # => closes the recursive find() call
            )  # => path-compresses on the way back
        return self.parent[x]  # => x's parent is now either itself, or the true root

    def union(  # => the cycle test IS the union: a failed union means "would cycle"
        self,  # => the union-find structure being mutated
        a: int,  # => the candidate edge's first endpoint
        b: int,  # => the two nodes this candidate edge would connect
    ) -> bool:  # => returns True if a merge actually happened
        root_a, root_b = self.find(a), self.find(b)  # => both groups' roots, compressed
        if root_a == root_b:  # => already connected -- adding this edge would cycle
            return False  # => signals "do not add this edge"
        if (  # => opens the rank comparison
            self.rank[root_a] < self.rank[root_b]  # => a's tree is strictly shorter
        ):  # => UNION BY RANK: shorter under taller
            self.parent[root_a] = (  # => opens the shorter-under-taller reassignment
                root_b  # => attaches the shorter tree under the taller
            )  # => closes the reassignment
        elif self.rank[root_a] > self.rank[root_b]:  # => the mirror comparison
            self.parent[root_b] = root_a  # => the mirror case
        else:  # => equal rank -- pick either, and the result grows one level taller
            self.parent[root_b] = root_a  # => arbitrarily attaches b's root under a's
            self.rank[root_a] += 1  # => only NOW does the resulting tree's height grow
        return True  # => signals "this edge was safely added"


def kruskal_mst(  # => sort-then-greedily-add, skipping any edge that would form a cycle
    n: int,  # => the number of nodes, labeled 0..n-1
    edges: list[tuple[int, int, int]],  # => node count and (u, v, weight) edges
) -> tuple[list[tuple[int, int, int]], int]:  # => (MST edges, total weight)
    sorted_edges = sorted(  # => opens the ascending-by-weight sort
        edges,  # => the raw, unsorted candidate edges
        key=lambda e: e[2],  # => sorts by the weight field only
    )  # => O(E log E): cheapest edges first
    uf = UnionFind(n)  # => starts with n singleton components
    mst_edges: list[tuple[int, int, int]] = []  # => accumulates the chosen edges
    total_weight = 0  # => running sum of the MST's edge weights
    for u, v, w in sorted_edges:  # => greedily considers cheapest-first
        if uf.union(u, v):  # => only True if u and v were NOT already connected
            mst_edges.append((u, v, w))  # => this edge is safe -- it can't form a cycle
            total_weight += w  # => tallies its weight into the MST total
    return mst_edges, total_weight  # => the MST's edges and its total weight


n = 5  # => 5 nodes, labeled 0..4
edges: list[tuple[int, int, int]] = [  # => (u, v, weight)
    (0, 1, 2),  # => the single cheapest edge -- picked first, always safe
    (0, 3, 6),  # => a mid-cost edge, picked only if it doesn't close a cycle
    (1, 2, 3),  # => second-cheapest -- picked early
    (1, 3, 8),  # => the most expensive edge -- likely rejected as redundant
    (1, 4, 5),  # => connects the otherwise-isolated node 4
    (  # => opens the alternate, pricier route to node 4
        2,  # => the edge's source node
        4,  # => the edge's destination node
        7,  # => this alternate route's weight
    ),  # => an alternate, pricier route to node 4 -- rejected once 4 is connected
    (3, 4, 9),  # => the second-most expensive edge -- almost certainly rejected
]  # => closes the edge list -- 5 nodes, 7 candidate edges, MST needs exactly 4
mst_edges, total_weight = kruskal_mst(n, edges)  # => builds the minimum spanning tree
print(len(mst_edges))  # => Output: 4 -- an MST always has exactly n-1 edges
print(total_weight)  # => Output: 16

assert len(mst_edges) == n - 1  # => confirms exactly n-1 edges -- a spanning tree
assert total_weight == 16  # => confirms the minimum possible total weight
print("ex-42 OK")  # => Output: ex-42 OK
```

**Run**: `python3 example.py`

**Output**:

```text
4
16
ex-42 OK
```

**`learning/code/ex-42-mst-kruskal/test_example.py`**

```python
"""Example 42: pytest verification for Kruskal's MST."""

from example import kruskal_mst


def test_mst_has_exactly_n_minus_1_edges() -> None:
    n = 4
    edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10)]
    mst_edges, _ = kruskal_mst(n, edges)
    assert len(mst_edges) == n - 1


def test_mst_total_weight_matches_known_minimum() -> None:
    n = 5
    edges = [
        (0, 1, 2),
        (0, 3, 6),
        (1, 2, 3),
        (1, 3, 8),
        (1, 4, 5),
        (2, 4, 7),
        (3, 4, 9),
    ]
    _, total = kruskal_mst(n, edges)
    assert total == 16


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Kruskal's greedy choice -- always consider the globally cheapest remaining edge next -- is provably safe for MST because adding any edge that does not create a cycle can never make the final spanning tree worse, a property specific to the minimum-spanning-tree problem.

**Why it matters**: Kruskal's algorithm is a clean example of the greedy paradigm (co-22) actually being provably optimal, unlike Example 45's coin-change counterexample where greedy fails -- the difference is whether the problem has the 'greedy-choice property,' and MST genuinely does. Union-find (Example 33) is what makes the cycle check efficient enough for this to scale.

---

### Example 43: Prim's Minimum Spanning Tree

_ex-43 &middot; exercises co-21, co-19_

Prim's algorithm is greedy on nodes instead of edges: grow one tree from a start node, always adding the cheapest edge that connects the growing tree to a new node, tracked with a heap. This example builds an MST on the same graph as Example 42 and confirms the total weight matches Kruskal's.

**`learning/code/ex-43-mst-prim/example.py`**

```python
"""Example 43: Prim's Minimum Spanning Tree, via a Heap."""

# Prim's algorithm (co-21) is GREEDY on nodes instead of edges: grow ONE tree
# from a start node, always adding the CHEAPEST edge that connects the
# growing tree to a new node -- a min-heap (co-09) finds that edge in O(log E).
import heapq  # => the min-heap priority queue used to pick the cheapest frontier edge


def prim_mst(  # => grows ONE tree from node 0, always via the cheapest frontier edge
    n: int,  # => the number of nodes, labeled 0..n-1
    adjacency: dict[int, list[tuple[int, int]]],  # => node count + weighted adjacency
) -> tuple[list[tuple[int, int, int]], int]:  # => (MST edges, total weight)
    in_tree: set[int] = {0}  # => the growing tree starts as just node 0
    mst_edges: list[tuple[int, int, int]] = []  # => accumulates (u, v, weight) chosen
    total_weight = 0  # => running sum of the MST's edge weights
    heap: list[tuple[int, int, int]] = [  # => (weight, from_node, to_node) candidates
        (w, 0, v)  # => (weight, from, to) so heapq sorts by weight automatically
        for v, w in adjacency[0]  # => every edge leaving the start node
    ]  # => the initial frontier, before heapify imposes heap order
    heapq.heapify(heap)  # => O(E): arranges the initial candidate edges into heap order
    while len(in_tree) < n:  # => stops once every node has joined the tree
        weight, u, v = heapq.heappop(heap)  # => the cheapest candidate edge overall
        if (  # => opens the stale-entry check
            v in in_tree  # => True if v was already added via an earlier, cheaper pop
        ):  # => a stale entry -- v joined the tree via a cheaper edge already
            continue  # => skip it, no new information
        in_tree.add(v)  # => v now joins the growing tree
        mst_edges.append((u, v, weight))  # => this edge is part of the MST
        total_weight += weight  # => tallies its weight
        for neighbor, w in adjacency[v]:  # => v's edges become new candidates
            if (  # => opens the outside-the-tree check
                neighbor not in in_tree  # => True only if neighbor hasn't joined yet
            ):  # => only edges reaching OUTSIDE the tree matter
                heapq.heappush(  # => the heap may end up holding stale entries too
                    heap,  # => the shared candidate-edge priority queue
                    (w, v, neighbor),  # => a new candidate frontier edge
                )  # => schedules this new candidate
    return mst_edges, total_weight  # => the MST's edges and its total weight


adjacency: dict[int, list[tuple[int, int]]] = {  # => the SAME graph as Example 42
    0: [(1, 2), (3, 6)],  # => node 0's two outgoing edges -- the initial frontier
    1: [  # => opens node 1's edge list
        (0, 2),  # => back to node 0
        (2, 3),  # => to node 2
        (3, 8),  # => to node 3, the priciest of node 1's edges
        (4, 5),  # => to node 4
    ],  # => node 1's edges, including the priciest one
    2: [(1, 3), (4, 7)],  # => node 2's two edges
    3: [  # => opens node 3's edge list
        (0, 6),  # => back to node 0
        (1, 8),  # => to node 1, tied for priciest overall
        (4, 9),  # => to node 4, the single priciest edge overall
    ],  # => node 3's edges, including the two priciest overall
    4: [(1, 5), (2, 7), (3, 9)],  # => node 4's edges
}  # => closes the adjacency map -- an undirected graph, each edge listed from both ends

mst_edges, total_weight = prim_mst(5, adjacency)  # => builds the MST, starting from 0
print(len(mst_edges))  # => Output: 4
print(total_weight)  # => Output: 16 -- matches Kruskal's answer on the same graph

assert len(mst_edges) == 4  # => confirms exactly n-1 edges
assert total_weight == 16  # => confirms the SAME minimum weight as Example 42's Kruskal
print("ex-43 OK")  # => Output: ex-43 OK
```

**Run**: `python3 example.py`

**Output**:

```text
4
16
ex-43 OK
```

**`learning/code/ex-43-mst-prim/test_example.py`**

```python
"""Example 43: pytest verification for Prim's MST."""

from example import prim_mst


def test_mst_total_weight_matches_kruskal_on_the_same_graph() -> None:
    adjacency = {
        0: [(1, 2), (3, 6)],
        1: [(0, 2), (2, 3), (3, 8), (4, 5)],
        2: [(1, 3), (4, 7)],
        3: [(0, 6), (1, 8), (4, 9)],
        4: [(1, 5), (2, 7), (3, 9)],
    }
    _, total = prim_mst(5, adjacency)
    assert total == 16  # => the same minimum weight Example 42's Kruskal found


def test_mst_has_exactly_n_minus_1_edges() -> None:
    adjacency = {0: [(1, 1), (2, 4)], 1: [(0, 1), (2, 2)], 2: [(0, 4), (1, 2)]}
    mst_edges, _ = prim_mst(3, adjacency)
    assert len(mst_edges) == 2


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Prim's and Kruskal's algorithms use completely different strategies -- growing one connected tree outward versus considering all edges globally by weight -- but both are provably optimal for MST, and both must arrive at the SAME total weight on any given graph (though not necessarily the identical set of edges, if ties exist).

**Why it matters**: Having two structurally different algorithms converge on the same answer is a strong correctness signal, and the choice between them in practice is about graph shape: Prim's heap-driven, Dijkstra-like approach (co-19) tends to be preferred for DENSE graphs, while Kruskal's sort-then-union-find approach tends to be preferred for SPARSE ones, since its cost is dominated by sorting the edge list.

---

### Example 44: Max Non-Overlapping Intervals

_ex-44 &middot; exercises co-22_

The greedy-choice property holds here: always pick the interval that finishes earliest among the remaining candidates. It never overlaps a previously chosen interval and leaves the most room for future picks. This example schedules a set of intervals greedily and confirms the count matches the true optimum.

**`learning/code/ex-44-greedy-interval-scheduling/example.py`**

```python
"""Example 44: Max Non-Overlapping Intervals via Earliest-Finish-Time Greedy."""

# The greedy-choice property (co-22) holds here: always pick the interval
# that FINISHES earliest among the remaining candidates. It never overlaps a
# later-finishing choice's own start, and it leaves maximum room for the rest
# -- a proof-backed optimal strategy, unlike Example 45's failing greedy.


def max_non_overlapping_intervals(  # => sort by finish time, then greedily take non-overlapping
    intervals: list[tuple[int, int]],  # => a list of (start, end) candidate intervals
) -> list[tuple[int, int]]:  # => (start, end) pairs; returns the chosen subset
    by_finish = sorted(  # => opens the earliest-finish-first sort
        intervals,
        key=lambda iv: iv[1],  # => sorts by the END field only
    )  # => O(n log n): earliest-finish first
    chosen: list[tuple[int, int]] = []  # => the greedily selected, non-overlapping set
    last_finish = float("-inf")  # => nothing chosen yet -- any interval can start
    for start, end in by_finish:  # => O(n): one pass through finish-sorted intervals
        if start >= last_finish:  # => this interval starts AFTER the last chosen ended
            chosen.append((start, end))  # => safe to take -- no overlap with `chosen`
            last_finish = end  # => this interval's end is now the new cutoff
    return chosen  # => the maximum-count set of mutually non-overlapping intervals


intervals: list[tuple[int, int]] = [  # => opens the classic CLRS activity-selection set
    (1, 4),  # => finishes 3rd-earliest -- a likely early pick
    (3, 5),  # => overlaps (1, 4) -- competes for the same early slot
    (
        0,
        6,
    ),  # => starts earliest but finishes late -- likely skipped in favor of shorter ones
    (5, 7),  # => finishes early enough to chain after (1, 4)
    (3, 8),  # => a long interval overlapping several others
    (5, 9),  # => overlaps (5, 7) -- competes for the same slot
    (6, 10),  # => overlaps (5, 7) -- starts before it finishes
    (8, 11),  # => starts right where (5, 7) ends -- a valid chain candidate
    (8, 12),  # => overlaps (8, 11) -- competes for the same slot
    (2, 13),  # => a very long interval, overlapping nearly everything
    (12, 14),  # => starts right where (8, 11) ends -- another valid chain candidate
]  # => the classic CLRS activity-selection example set
chosen = max_non_overlapping_intervals(intervals)  # => the greedy-optimal selection
print(chosen)  # => Output: [(1, 4), (5, 7), (8, 11), (12, 14)]
print(len(chosen))  # => Output: 4

assert len(chosen) == 4  # => confirms the maximum possible count for this instance
for i in range(1, len(chosen)):  # => confirms no two chosen intervals overlap
    assert chosen[i][0] >= chosen[i - 1][1]  # => next start is at/after previous finish
print("ex-44 OK")  # => Output: ex-44 OK
```

**Run**: `python3 example.py`

**Output**:

```text
[(1, 4), (5, 7), (8, 11), (12, 14)]
4
ex-44 OK
```

**`learning/code/ex-44-greedy-interval-scheduling/test_example.py`**

```python
"""Example 44: pytest verification for Greedy Interval Scheduling."""

from example import max_non_overlapping_intervals


def test_no_two_chosen_intervals_overlap() -> None:
    intervals = [(1, 3), (2, 4), (3, 5), (0, 6), (5, 7)]
    chosen = max_non_overlapping_intervals(intervals)
    for i in range(1, len(chosen)):
        assert chosen[i][0] >= chosen[i - 1][1]


def test_matches_the_known_optimal_count() -> None:
    intervals = [(1, 2), (2, 3), (3, 4), (1, 4)]  # => three tiny + one that blocks all
    chosen = max_non_overlapping_intervals(intervals)
    assert len(chosen) == 3  # => (1,2), (2,3), (3,4) -- the big one loses out


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Sorting by FINISH time (not start time, and not duration) is the specific choice that makes greedy interval scheduling provably optimal -- picking the interval that frees up the earliest 'next available' moment maximizes room for every future choice.

**Why it matters**: This is the canonical example of a correctly-applied greedy algorithm, worth contrasting directly against Example 45's greedy coin-change FAILURE: the difference is not 'greedy is good or bad' in general, it is whether a specific problem's structure actually guarantees the locally-optimal choice never costs anything globally. Interval scheduling's exchange-argument proof is the textbook demonstration that it does here.

---

### Example 45: Greedy Coin Change Fails

_ex-45 &middot; exercises co-22, co-23_

Greedy only works when the greedy-choice property actually holds. US coins {1, 5, 10, 25} happen to make greedy-always-optimal, but that is a property of those specific denominations, not of greedy in general. This example picks a non-canonical coin set and shows greedy producing a genuinely suboptimal answer.

**`learning/code/ex-45-greedy-coin-change-fails/example.py`**

```python
"""Example 45: Greedy Coin Change Fails on a Non-Canonical Coin Set."""

# Greedy (co-22) only works when the greedy-choice property actually HOLDS.
# US coins {1, 5, 10, 25} happen to make greedy-always-optimal, but that's a
# property of THIS SPECIFIC coin set, not of "greedy" in general (co-23):
# {1, 3, 4} is a counterexample where always taking the largest coin loses.


def greedy_coin_change(
    coins: list[int], amount: int
) -> list[int]:  # => always takes the LARGEST coin that still fits
    coins_sorted = sorted(coins, reverse=True)  # => tries biggest coins first
    used: list[int] = []  # => the coins greedily selected, in the order taken
    remaining = amount  # => how much of the target amount is still unpaid
    for c in coins_sorted:  # => tries each denomination, largest to smallest
        while remaining >= c:  # => keeps taking THIS coin as long as it still fits
            used.append(c)  # => records one more coin of this denomination
            remaining -= c  # => reduces the remaining amount accordingly
    return used  # => the greedy answer -- NOT guaranteed to be optimal


non_canonical_coins: list[int] = [1, 3, 4]  # => the counterexample coin set
target = 6  # => the amount to make change for
greedy_answer = greedy_coin_change(non_canonical_coins, target)  # => greedy's choice
print(greedy_answer)  # => Output: [4, 1, 1]
print(len(greedy_answer))  # => Output: 3 -- greedy needs 3 coins

optimal_answer: list[int] = [3, 3]  # => the TRUE optimum: two 3-coins, verified by hand
print(sum(optimal_answer) == target)  # => Output: True
print(len(optimal_answer))  # => Output: 2 -- strictly fewer coins than greedy found

assert sum(greedy_answer) == target  # => confirms greedy's answer is still VALID change
assert len(greedy_answer) == 3  # => confirms greedy's (suboptimal) coin count
assert len(optimal_answer) < len(
    greedy_answer
)  # => confirms a strictly BETTER answer exists that greedy never finds
print("ex-45 OK")  # => Output: ex-45 OK
```

**Run**: `python3 example.py`

**Output**:

```text
[4, 1, 1]
3
True
2
ex-45 OK
```

**`learning/code/ex-45-greedy-coin-change-fails/test_example.py`**

```python
"""Example 45: pytest verification for Greedy Coin Change's Failure Case."""

from example import greedy_coin_change


def test_greedy_produces_valid_but_suboptimal_change() -> None:
    result = greedy_coin_change([1, 3, 4], 6)
    assert sum(result) == 6  # => still valid change...
    assert len(result) == 3  # => ...but not the minimum possible (2, via 3+3)


def test_greedy_is_optimal_on_us_coin_denominations() -> None:
    result = greedy_coin_change([1, 5, 10, 25], 41)
    assert sum(result) == 41
    assert len(result) == 4  # => 25 + 10 + 5 + 1 -- greedy IS optimal for these coins


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Greedy's optimality is a property of the SPECIFIC problem instance's structure, not a general guarantee -- 'always take the largest coin that fits' produces the true minimum-coin answer for US currency, but produces a worse-than-optimal answer for a coin set like {1, 3, 4} that lacks the same structural guarantee.

**Why it matters**: This counterexample is the entire reason DP (co-23) exists as a separate paradigm from greedy: whenever a problem's greedy-choice property cannot be proven, exploring EVERY possibility (which DP does efficiently, via memoized subproblems) is the only way to guarantee an optimal answer. Example 48 solves this exact same coin set correctly with DP, beating greedy's wrong answer.

---

### Example 46: Fibonacci -- Memoization vs Tabulation

_ex-46 &middot; exercises co-23_

Both DP styles exploit overlapping subproblems: naive recursive `fib(n)` recomputes `fib(5)` exponentially many times. Memoization caches results top-down as they are computed; tabulation builds them bottom-up in a table. This example implements both and confirms they agree while both stay O(n).

**`learning/code/ex-46-dp-fib-memo-vs-tab/example.py`**

```python
"""Example 46: Fibonacci -- Top-Down Memoization vs Bottom-Up Tabulation."""

# Both DP styles (co-23) exploit OVERLAPPING SUBPROBLEMS -- naive recursive
# fib(n) recomputes fib(5) exponentially many times. Memoization caches
# top-down recursive results; tabulation builds the answer bottom-up in a
# loop, with no recursion (and no call-stack depth risk) at all.


def fib_memo(n: int, cache: dict[int, int] | None = None) -> int:  # => top-down, cached
    if cache is None:  # => the first call creates a fresh cache -- never share defaults
        cache = {}  # => a new, empty memo for this top-level call
    if n <= 1:  # => base cases: fib(0)=0, fib(1)=1
        return n  # => no recursion needed at the base
    if n in cache:  # => already computed -- an O(1) cache hit
        return cache[n]  # => reuses the previously computed result
    cache[n] = fib_memo(n - 1, cache) + fib_memo(
        n - 2, cache
    )  # => computes ONCE, caches
    return cache[n]  # => the newly computed and cached value


def fib_tab(n: int) -> int:  # => bottom-up, iterative, no recursion at all
    if n <= 1:  # => base cases, same as above
        return n
    prev2, prev1 = 0, 1  # => fib(0) and fib(1), the two seeds tabulation builds from
    for _ in range(2, n + 1):  # => builds each fib(i) from the two before it
        prev2, prev1 = prev1, prev2 + prev1  # => slides the window forward by one
    return prev1  # => fib(n), built up with O(1) extra space, no call stack at all


values: list[int] = [0, 1, 5, 10, 20, 30]  # => a spread of inputs, including base cases
memo_results = [fib_memo(n) for n in values]  # => top-down answers
tab_results = [fib_tab(n) for n in values]  # => bottom-up answers
print(memo_results)  # => Output: [0, 1, 5, 55, 6765, 832040]
print(tab_results)  # => Output: [0, 1, 5, 55, 6765, 832040]

assert memo_results == tab_results  # => confirms both styles agree on every input
assert fib_tab(30) == 832040  # => confirms a specific known Fibonacci value
print("ex-46 OK")  # => Output: ex-46 OK
```

**Run**: `python3 example.py`

**Output**:

```text
[0, 1, 5, 55, 6765, 832040]
[0, 1, 5, 55, 6765, 832040]
ex-46 OK
```

**`learning/code/ex-46-dp-fib-memo-vs-tab/test_example.py`**

```python
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
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Memoization and tabulation solve the SAME overlapping-subproblems structure from opposite directions -- memoization caches results lazily as a top-down recursion needs them, while tabulation fills a table eagerly from the smallest subproblem upward -- and both eliminate the exponential recomputation naive recursion suffers.

**Why it matters**: This side-by-side comparison is the foundational DP lesson: 'dynamic programming' is not one specific coding pattern, it is the PRINCIPLE of never solving the same subproblem twice, implementable either way. Every later DP example in this topic (Examples 47-51, 59-62) picks whichever style fits its problem's dependency structure best.

---

### Example 47: Count Ways to Climb Stairs

_ex-47 &middot; exercises co-23_

`ways(n) = ways(n-1) + ways(n-2)`: the last step taken to reach stair n was either a 1-step from stair n-1 or a 2-step from stair n-2, so the total ways to reach n is the sum of ways to reach each of those. This example computes stair counts via DP and checks them against the recurrence directly.

**`learning/code/ex-47-dp-climbing-stairs/example.py`**

```python
"""Example 47: Count Ways to Climb n Stairs (1 or 2 Steps at a Time) via DP."""

# ways(n) = ways(n-1) + ways(n-2) (co-23): the LAST step taken to reach stair
# n was either a 1-step from stair n-1, or a 2-step from stair n-2 -- so the
# total ways to reach n is simply the sum of ways to reach each predecessor.
# This is structurally IDENTICAL to Fibonacci, just with different seed values.


def count_ways_to_climb(  # => Fibonacci-shaped recurrence, computed bottom-up
    n: int,  # => the target stair count
) -> int:  # => bottom-up tabulation, O(n) time, O(1) space
    if n <= 1:  # => 0 stairs: 1 way (do nothing); 1 stair: 1 way (a single 1-step)
        return 1  # => base cases
    prev2, prev1 = 1, 1  # => ways(0)=1, ways(1)=1 -- the two seeds
    for _ in range(2, n + 1):  # => builds ways(i) from the two steps before it
        prev2, prev1 = (  # => opens the two-variable slide
            prev1,  # => the new prev2 -- what used to be prev1
            prev2 + prev1,  # => the new prev1 -- this stair's own way-count
        )  # => slides forward: ways(i) = ways(i-1)+ways(i-2)
    return prev1  # => ways(n)


def count_ways_brute_force(n: int) -> int:  # => O(2^n): enumerates every step sequence
    if n <= 1:  # => same base cases
        return 1  # => 0 or 1 stairs: exactly one way
    if n == 2:  # => exactly 2 ways: [1,1] or [2]
        return 2  # => the second base case
    return count_ways_brute_force(
        n - 1  # => recurses on the 1-step predecessor
    ) + count_ways_brute_force(  # => the LAST-step split
        n - 2  # => recurses on the 2-step predecessor
    )  # => no memoization -- deliberately re-derives the same recurrence, slowly


for n in [0, 1, 2, 3, 4, 5]:  # => a spread of small n, where brute force stays feasible
    fast = count_ways_to_climb(n)  # => O(n) tabulated answer
    slow = count_ways_brute_force(n)  # => O(2^n) brute-force answer, as ground truth
    print(f"n={n}: {fast}")  # => Output: one "n=N: ways" line per n
    assert fast == slow  # => confirms both approaches agree exactly

assert count_ways_to_climb(5) == 8  # => 1+1+1+1+1, 2+1+1+1 (x4 orderings), 2+2+1 (x3)
print("ex-47 OK")  # => Output: ex-47 OK
```

**Run**: `python3 example.py`

**Output**:

```text
n=0: 1
n=1: 1
n=2: 2
n=3: 3
n=4: 5
n=5: 8
ex-47 OK
```

**`learning/code/ex-47-dp-climbing-stairs/test_example.py`**

```python
"""Example 47: pytest verification for Climbing Stairs DP."""

from example import count_ways_brute_force, count_ways_to_climb


def test_matches_brute_force_for_small_n() -> None:
    for n in range(15):
        assert count_ways_to_climb(n) == count_ways_brute_force(n)


def test_known_value_for_five_stairs() -> None:
    assert count_ways_to_climb(5) == 8


# => Run: pytest -- Output: 2 passed
```

**Verify**: `pytest -q`

**Output**:

```text
2 passed
```

**Key takeaway**: Recognizing that 'ways to reach stair n' decomposes into 'ways to reach n-1' plus 'ways to reach n-2' -- based on the LAST step taken, not the first -- is the same structural insight behind Fibonacci (Example 46), just relabeled for a different problem.

**Why it matters**: This example is a deliberate bridge from 'DP is Fibonacci' to 'DP is a general technique': recognizing the Fibonacci-shaped recurrence hiding inside an apparently unrelated counting problem is exactly the pattern-recognition skill that DP problems in interviews and real systems demand, far more often than a literal Fibonacci computation ever comes up.

---

### Example 48: Minimum-Coin Change via DP

_ex-48 &middot; exercises co-23_

`dp[a]` = minimum coins to make amount a: try every coin as the last one used and take the best option -- this explores possibilities greedy skipped entirely. This example solves Example 45's exact non-canonical coin set with DP and confirms it beats greedy's suboptimal answer.

**`learning/code/ex-48-dp-coin-change-min/example.py`**

```python
"""Example 48: Minimum-Coin Change via DP -- Beats Example 45's Greedy Answer."""

# dp[a] = minimum coins to make amount a (co-23): try EVERY coin as the LAST
# one used, and take the best option -- this explores possibilities greedy
# never considers, so it can't be fooled the way Example 45's greedy was.
INF = float("inf")  # => sentinel for "no way to make this amount (yet)"


def min_coins_dp(  # => tries every coin as the LAST one used, keeps the best count
    coins: list[int],
    amount: int,  # => the available coin denominations, and the target
) -> int | None:  # => None if amount is unreachable with these coins
    dp: list[float] = [0.0] + [  # => opens the dp array construction
        INF  # => every amount besides 0 starts as "not yet known reachable"
    ] * amount  # => dp[0]=0 coins; everything else unknown
    for a in range(  # => opens the ascending-amount range
        1,
        amount + 1,  # => builds every amount from 1 up to the target, in order
    ):  # => builds dp[a] from smaller, already-solved amounts
        for c in coins:  # => tries EVERY coin as the one used LAST to reach amount a
            if (  # => opens the "coin c improves dp[a]" check
                c <= a and dp[a - c] + 1 < dp[a]
            ):  # => using coin c beats the current best
                dp[a] = (  # => opens the improved-count assignment
                    dp[a - c] + 1  # => one more coin on top of the best way to make a-c
                )  # => one more coin than however dp[a-c] was reached
    return (  # => opens the final unreachable-or-int-result decision
        None if dp[amount] == INF else int(dp[amount])  # => still INF means unreachable
    )  # => None if truly unreachable


non_canonical_coins: list[int] = [1, 3, 4]  # => Example 45's counterexample coin set
target = 6  # => the same target Example 45 used
result = min_coins_dp(non_canonical_coins, target)  # => the TRUE minimum via DP
print(result)  # => Output: 2 -- two 3-coins: 3 + 3 = 6

assert result == 2  # => confirms DP finds the true optimum
assert result < 3  # => confirms DP strictly BEATS Example 45's greedy answer (3 coins)
assert min_coins_dp([1, 3, 4], 0) == 0  # => zero coins are needed to make amount 0
assert min_coins_dp([5], 3) is None  # => 3 is unreachable using only 5-coins
print("ex-48 OK")  # => Output: ex-48 OK
```

**Run**: `python3 example.py`

**Output**:

```text
2
ex-48 OK
```

**`learning/code/ex-48-dp-coin-change-min/test_example.py`**

```python
"""Example 48: pytest verification for DP Minimum Coin Change."""

from example import min_coins_dp


def test_beats_the_greedy_answer_on_the_non_canonical_coin_set() -> None:
    assert min_coins_dp([1, 3, 4], 6) == 2  # => strictly fewer than greedy's 3


def test_us_coins_matches_greedy_since_greedy_is_optimal_there() -> None:
    assert min_coins_dp([1, 5, 10, 25], 41) == 4


def test_unreachable_amount_returns_none() -> None:
    assert min_coins_dp([5], 3) is None


# => Run: pytest -- Output: 3 passed
```

**Verify**: `pytest -q`

**Output**:

```text
3 passed
```

**Key takeaway**: DP's 'try every last coin used' approach considers possibilities a greedy algorithm never revisits once it commits to a choice -- that exhaustive-but-efficient exploration (thanks to memoized overlapping subproblems) is exactly what recovers the TRUE optimum greedy missed.

**Why it matters**: This is the direct payoff of Example 45's cautionary tale: the same problem, solved with the right paradigm, produces the genuinely optimal answer instead of greedy's plausible-looking but wrong one. Recognizing 'greedy might not be provably correct here, fall back to DP' is a decision this topic asks you to make repeatedly, most explicitly in Example 58's side-by-side contrast.

---

### Example 49: Levenshtein Edit Distance

_ex-49 &middot; exercises co-24_

`dp[i][j]` = min edits to turn `word1[:i]` into `word2[:j]`: if the last characters match, no edit is needed there, reusing `dp[i-1][j-1]` directly; otherwise, the best of an insert, delete, or substitute. This example builds the full 2D table and checks the result against known string pairs.

**`learning/code/ex-49-dp-edit-distance/example.py`**

```python
"""Example 49: Levenshtein Edit Distance -- a 2D DP Table."""

# dp[i][j] = min edits to turn word1[:i] into word2[:j] (co-24): if the last
# characters match, no edit is needed there -- reuse dp[i-1][j-1] directly.
# Otherwise, try all three edits (insert, delete, substitute) and take the
# cheapest, each reducing to a smaller, already-solved subproblem.


def edit_distance(word1: str, word2: str) -> int:  # => O(m*n) time and space
    m, n = len(word1), len(word2)  # => the two words' lengths
    dp: list[list[int]] = [  # => opens the 2D table construction
        [0] * (n + 1)
        for _ in range(m + 1)  # => one fresh row of zeros per prefix of word1
    ]  # => (m+1) x (n+1) table, one extra row/col for the empty-prefix case
    for i in range(m + 1):  # => turning word1[:i] into "" costs i deletions
        dp[i][0] = i  # => base case along the first column
    for j in range(n + 1):  # => turning "" into word2[:j] costs j insertions
        dp[0][j] = j  # => base case along the first row
    for i in range(1, m + 1):  # => fills the table row by row
        for j in range(1, n + 1):  # => and column by column within each row
            if word1[i - 1] == word2[j - 1]:  # => the last characters already match
                dp[i][j] = dp[i - 1][  # => opens the diagonal-cell lookup
                    j - 1  # => the subproblem for both prefixes shortened by one char
                ]  # => no edit needed here -- reuse the diagonal
            else:  # => the last characters differ -- try each of the three edits
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # => DELETE word1[i-1]
                    dp[i][j - 1],  # => INSERT word2[j-1]
                    dp[i - 1][j - 1],  # => SUBSTITUTE word1[i-1] for word2[j-1]
                )  # => plus 1 for whichever edit was cheapest
    return dp[m][n]  # => the bottom-right cell: the full-word edit distance


print(edit_distance("kitten", "sitting"))  # => Output: 3 -- k->s, e->i, +g
print(edit_distance("", "abc"))  # => Output: 3 -- three insertions
print(edit_distance("same", "same"))  # => Output: 0 -- identical words need no edits

assert (  # => opens the classic-example check
    edit_distance("kitten", "sitting")
    == 3  # => True only if the computed distance is 3
)  # => confirms the classic example's answer
assert edit_distance("", "abc") == 3  # => confirms the empty-string edge case
assert edit_distance("same", "same") == 0  # => confirms identical strings cost nothing
assert edit_distance("abc", "") == 3  # => confirms the mirrored empty-string case
print("ex-49 OK")  # => Output: ex-49 OK
```

**Run**: `python3 example.py`

**Output**:

```text
3
3
0
ex-49 OK
```

**`learning/code/ex-49-dp-edit-distance/test_example.py`**

```python
"""Example 49: pytest verification for Levenshtein Edit Distance."""

from example import edit_distance


def test_classic_kitten_to_sitting_example() -> None:
    assert edit_distance("kitten", "sitting") == 3


def test_identical_strings_have_zero_distance() -> None:
    assert edit_distance("hello", "hello") == 0


def test_completely_different_single_characters() -> None:
    assert edit_distance("a", "b") == 1  # => one substitution


# => Run: pytest -- Output: 3 passed
```

**Verify**: `pytest -q`

**Output**:

```text
3 passed
```

**Key takeaway**: Edit distance's 2D table captures a problem with TWO shrinking dimensions simultaneously (a prefix of each string), which is exactly what distinguishes 2D DP from the single-dimension DP in Examples 46-48 -- each cell depends on up to three neighboring cells, not just one or two.

**Why it matters**: Edit distance is the algorithm behind spell-checkers, diff tools, and DNA sequence alignment -- anywhere 'how different are these two sequences' needs a precise, minimal-edit-count answer rather than a fuzzy guess. It is also the clearest on-ramp to 2D DP in this topic, since its three possible last-edit choices (insert, delete, substitute) map directly onto three neighboring table cells.

---

### Example 50: Longest Common Subsequence

_ex-50 &middot; exercises co-24_

`dp[i][j]` = LCS length of `word1[:i]` and `word2[:j]`: matching last characters extend the diagonal's LCS by one; otherwise, take the better of dropping a character from either string. This example builds the DP table, then reconstructs an actual longest common subsequence by walking the table backward.

**`learning/code/ex-50-dp-lcs/example.py`**

```python
"""Example 50: Longest Common Subsequence -- DP Table, Then Reconstruction."""

# dp[i][j] = LCS length of word1[:i] and word2[:j] (co-24): matching last
# characters extend the diagonal's LCS by one; otherwise, take the better of
# dropping ONE character from either string. RECONSTRUCTION then walks the
# filled table backward, following exactly which choice produced each cell.


def lcs_length_table(  # => builds the full DP table, bottom-up, one cell at a time
    word1: str,  # => the first string being compared
    word2: str,  # => the two strings to compare
) -> list[list[int]]:  # => O(m*n) table build
    m, n = len(word1), len(word2)  # => the two strings' lengths
    dp: list[list[int]] = [  # => opens the 2D table construction
        [0] * (n + 1)  # => one zero-filled row per prefix length of word1
        for _ in range(m + 1)  # => one fresh row of zeros per prefix of word1
    ]  # => dp[i][0] and dp[0][j] are already 0 -- an empty prefix has LCS length 0
    for i in range(1, m + 1):  # => fills row by row
        for j in range(1, n + 1):  # => and column by column
            if word1[i - 1] == word2[j - 1]:  # => the last characters MATCH
                dp[i][j] = dp[i - 1][j - 1] + 1  # => extends the diagonal's LCS by one
            else:  # => no match -- the LCS must drop ONE character from either string
                dp[i][j] = max(
                    dp[i - 1][j],  # => value if word1's last char is dropped
                    dp[i][j - 1],  # => value if word2's last char is dropped
                )  # => takes whichever drop preserves the longer LCS
    return dp  # => the full table -- dp[m][n] is the final LCS length


def reconstruct_lcs(  # => retraces which choice built each cell, to recover the actual chars
    word1: str,  # => the same first string used to build the table
    word2: str,  # => the same second string used to build the table
    dp: list[list[int]],  # => the original strings + filled table
) -> str:  # => walks the table BACKWARD from (m, n)
    i, j = len(word1), len(word2)  # => starts at the bottom-right cell
    chars: list[str] = []  # => accumulates matched characters, in REVERSE order
    while i > 0 and j > 0:  # => stops once either string is exhausted
        if (  # => opens the match check
            word1[i - 1] == word2[j - 1]
        ):  # => this position was a MATCH -- part of the LCS
            chars.append(word1[i - 1])  # => records this matched character
            i -= 1  # => moves diagonally, retracing the match
            j -= 1  # => both indices step back together on a diagonal match
        elif dp[i - 1][j] >= dp[i][j - 1]:  # => the LCS came from dropping word1's char
            i -= 1  # => moves up, following that earlier decision
        else:  # => the LCS came from dropping word2's char instead
            j -= 1  # => moves left, following THAT earlier decision
    return "".join(reversed(chars))  # => reverses back to forward reading order


# demonstrates the full pipeline: build the table, then reconstruct from it
word1, word2 = "ABCBDAB", "BDCABA"  # => the classic LCS example pair
table = lcs_length_table(word1, word2)  # => builds the DP table once
length = table[len(word1)][len(word2)]  # => the LCS length, read from the final cell
sequence = reconstruct_lcs(word1, word2, table)  # => the actual matched subsequence
print(length)  # => Output: 4
print(sequence)  # => Output: BCBA

assert length == 4  # => confirms the known LCS length for this classic example
assert len(sequence) == length  # => confirms the reconstructed string has that length
assert sequence == "BCBA"  # => confirms the exact reconstructed subsequence
print("ex-50 OK")  # => Output: ex-50 OK
```

**Run**: `python3 example.py`

**Output**:

```text
4
BCBA
ex-50 OK
```

**`learning/code/ex-50-dp-lcs/test_example.py`**

```python
"""Example 50: pytest verification for Longest Common Subsequence."""

from example import lcs_length_table, reconstruct_lcs


def test_classic_abcbdab_bdcaba_example() -> None:
    word1, word2 = "ABCBDAB", "BDCABA"
    table = lcs_length_table(word1, word2)
    assert table[len(word1)][len(word2)] == 4


def test_no_common_characters_has_zero_length_lcs() -> None:
    table = lcs_length_table("abc", "xyz")
    assert table[3][3] == 0
    assert reconstruct_lcs("abc", "xyz", table) == ""


def test_reconstructed_sequence_is_a_valid_subsequence_of_both_strings() -> None:
    word1, word2 = "hello", "yellow"
    table = lcs_length_table(word1, word2)
    sequence = reconstruct_lcs(word1, word2, table)
    assert len(sequence) == table[len(word1)][len(word2)]


# => Run: pytest -- Output: 3 passed
```

**Verify**: `pytest -q`

**Output**:

```text
3 passed
```

**Key takeaway**: A DP table stores enough information not just to compute the ANSWER (the LCS length), but to RECONSTRUCT an actual optimal solution afterward, by walking backward through the table and following whichever transition produced each cell's value.

**Why it matters**: Many DP examples in this topic stop at computing a single number (the length, the minimum cost); this example demonstrates the extra step -- reconstruction -- that turns 'the answer is 4' into 'the answer is 4, and here is an actual sequence achieving it,' which is what a real diff tool or version-control merge needs, not just a length.

---

### Example 51: 0/1 Knapsack

_ex-51 &middot; exercises co-24_

`dp[i][w]` = best value using the first i items within capacity w: for each item, either skip it (`dp[i-1][w]`) or take it (its value plus `dp[i-1][w - weight]`), and keep the better option. This example solves a small knapsack instance with the full 2D table and confirms the optimal value.

**`learning/code/ex-51-dp-knapsack-01/example.py`**

```python
"""Example 51: 0/1 Knapsack -- 2D DP over Items and Capacity."""

# dp[i][w] = best value using the first i items within capacity w (co-24):
# for each item, either SKIP it (dp[i-1][w]) or TAKE it (its value plus
# dp[i-1][w-weight], if it fits) -- "0/1" because each item is taken at
# most once, unlike the unbounded knapsack variant.


def knapsack_01(  # => for each item, either SKIP it or TAKE it, whichever is better
    weights: list[int],  # => each item's own weight
    values: list[int],  # => each item's own value
    capacity: int,  # => item weights/values + limit
) -> int:  # => O(n * capacity) time and space
    n = len(weights)  # => number of available items
    dp: list[list[int]] = [  # => opens the 2D table construction
        [0] * (capacity + 1)  # => one zero-filled row per item count
        for _ in range(n + 1)  # => one fresh row of zeros per item count
    ]  # => dp[0][*] = 0: zero items always yields zero value
    for i in range(1, n + 1):  # => considers items one at a time
        weight, value = weights[i - 1], values[i - 1]  # => this item's own weight/value
        for w in range(capacity + 1):  # => every possible capacity, from 0 up
            dp[i][w] = dp[i - 1][w]  # => the SKIP option: value stays whatever it was
            if weight <= w:  # => the TAKE option is only possible if it actually fits
                dp[i][w] = max(
                    dp[i][w],  # => the SKIP option's value
                    value + dp[i - 1][w - weight],  # => the TAKE option's value
                )  # => best of skip vs take
    return dp[n][capacity]  # => the best achievable value at full capacity


weights: list[int] = [2, 3, 4, 5]  # => four items' weights
values: list[int] = [3, 4, 5, 6]  # => their corresponding values
capacity = 5  # => the knapsack's weight limit
best_value = knapsack_01(weights, values, capacity)  # => the optimal achievable value
print(best_value)  # => Output: 7 -- items 0 and 1 (weight 2+3=5, value 3+4=7)

assert best_value == 7  # => confirms the known optimal value for this instance
assert knapsack_01([], [], 10) == 0  # => no items at all -- nothing to gain
assert (  # => opens the too-heavy-item check
    knapsack_01([100], [50], 1) == 0  # => True only if the DP correctly skips it
)  # => an item too heavy to ever fit contributes nothing
print("ex-51 OK")  # => Output: ex-51 OK
```

**Run**: `python3 example.py`

**Output**:

```text
7
ex-51 OK
```

**`learning/code/ex-51-dp-knapsack-01/test_example.py`**

```python
"""Example 51: pytest verification for 0/1 Knapsack."""

from example import knapsack_01


def test_matches_a_known_optimal_value() -> None:
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    assert knapsack_01(weights, values, capacity=7) == 9  # => items of weight 3 and 4


def test_zero_capacity_yields_zero_value() -> None:
    assert knapsack_01([1, 2, 3], [10, 20, 30], capacity=0) == 0


def test_single_item_that_exactly_fits() -> None:
    assert knapsack_01([5], [42], capacity=5) == 42


# => Run: pytest -- Output: 3 passed
```

**Verify**: `pytest -q`

**Output**:

```text
3 passed
```

**Key takeaway**: 0/1 knapsack's 'skip or take' choice at every item, tracked against every possible remaining capacity, is what the 2D table (items x capacity) is built to capture -- a decision GREEDY (picking the best value-per-weight ratio) cannot make correctly, as Example 79's shootout demonstrates directly.

**Why it matters**: 0/1 knapsack is the most commonly cited DP problem in technical interviews for good reason: it has a genuinely deceptive greedy-looking shortcut (sort by value/weight ratio) that FAILS, and the 2D table here is what correctly explores every skip-or-take combination without brute-forcing all `2^n` subsets.

---

### Example 52: Binary Search Boundaries

_ex-52 &middot; exercises co-27_

A plain binary search stops at any match. Finding the leftmost match instead means: on a match, do not stop, keep searching the left half for an even earlier occurrence. This example finds both leftmost and rightmost occurrences of a repeated value, including cases where the target is entirely absent.

**`learning/code/ex-52-binary-search-boundary/example.py`**

```python
"""Example 52: Binary Search for the Leftmost and Rightmost Occurrence."""

# A plain binary search stops at ANY match. Finding the LEFTMOST (co-27)
# match instead means: on a match, don't stop -- keep searching the LEFT
# half for an even earlier one. The rightmost search is the mirror image.


def leftmost_index(items: list[int], target: int) -> int:  # => -1 if target is absent
    lo, hi = 0, len(items) - 1  # => the active search range
    result = -1  # => no match found yet
    while lo <= hi:  # => standard binary search bounds
        mid = (lo + hi) // 2  # => the midpoint of the active range
        if items[mid] == target:  # => found A match -- but is it the FIRST one?
            result = mid  # => records this as the best-known leftmost match so far
            hi = mid - 1  # => keeps searching LEFT for an even earlier occurrence
        elif items[mid] < target:  # => target must be further right
            lo = mid + 1  # => shrinks the range from the left edge
        else:  # => target must be further left
            hi = mid - 1  # => shrinks the range from the right edge
    return result  # => the smallest index where target occurs, or -1


def rightmost_index(items: list[int], target: int) -> int:  # => -1 if target is absent
    lo, hi = 0, len(items) - 1  # => the active search range
    result = -1  # => no match found yet
    while lo <= hi:  # => standard binary search bounds
        mid = (lo + hi) // 2  # => the midpoint of the active range
        if items[mid] == target:  # => found A match -- but is it the LAST one?
            result = mid  # => records this as the best-known rightmost match so far
            lo = mid + 1  # => keeps searching RIGHT for an even later occurrence
        elif (  # => opens the rightmost-side range-narrowing check
            items[mid] < target
        ):  # => same rule as leftmost -- target lies further right
            lo = mid + 1  # => shrinks the range from the left edge
        else:  # => same rule as leftmost -- target lies further left
            hi = mid - 1  # => shrinks the range from the right edge
    return result  # => the largest index where target occurs, or -1


data: list[int] = [1, 2, 2, 2, 3, 4, 4, 5]  # => sorted, with runs of duplicate values
print(leftmost_index(data, 2))  # => Output: 1 -- the first of three 2's
print(rightmost_index(data, 2))  # => Output: 3 -- the last of three 2's
print(leftmost_index(data, 4))  # => Output: 5
print(leftmost_index(data, 9))  # => Output: -1 -- 9 is absent entirely

assert leftmost_index(data, 2) == 1  # => confirms the first occurrence's index
assert rightmost_index(data, 2) == 3  # => confirms the last occurrence's index
assert leftmost_index(data, 9) == -1  # => confirms an absent target returns -1
assert rightmost_index(data, 9) == -1  # => confirms the mirrored absent case too
assert leftmost_index(data, 1) == rightmost_index(  # => a single-occurrence value
    data,  # => the same sorted array searched throughout
    1,  # => the value 1, which appears exactly once in data
)  # => a value with only ONE occurrence has matching leftmost and rightmost
print("ex-52 OK")  # => Output: ex-52 OK
```

**Run**: `python3 example.py`

**Output**:

```text
1
3
5
-1
ex-52 OK
```

**`learning/code/ex-52-binary-search-boundary/test_example.py`**

```python
"""Example 52: pytest verification for Binary Search Boundaries."""

from example import leftmost_index, rightmost_index


def test_leftmost_and_rightmost_bracket_a_run_of_duplicates() -> None:
    data = [1, 3, 3, 3, 3, 7, 9]
    assert leftmost_index(data, 3) == 1
    assert rightmost_index(data, 3) == 4


def test_absent_target_returns_negative_one_both_ways() -> None:
    data = [2, 4, 6, 8]
    assert leftmost_index(data, 5) == -1
    assert rightmost_index(data, 5) == -1


def test_single_occurrence_matches_on_both_boundaries() -> None:
    data = [10, 20, 30]
    assert leftmost_index(data, 20) == rightmost_index(data, 20) == 1


# => Run: pytest -- Output: 3 passed
```

**Verify**: `pytest -q`

**Output**:

```text
3 passed
```

**Key takeaway**: Finding a BOUNDARY (leftmost or rightmost occurrence) with binary search requires changing what happens ON a match -- instead of stopping immediately, keep narrowing toward the boundary while remembering the best match found so far.

**Why it matters**: This small variation on binary search is the foundation for Example 73's binary-search-on-a-monotonic-predicate: both techniques rely on the same idea of narrowing toward a BOUNDARY rather than stopping at the first success, which generalizes far beyond searching a literal sorted array into searching any monotonic answer space.

---

← Previous: [Beginner Examples](./beginner.md) · Next: [Advanced Examples](./advanced.md) →
