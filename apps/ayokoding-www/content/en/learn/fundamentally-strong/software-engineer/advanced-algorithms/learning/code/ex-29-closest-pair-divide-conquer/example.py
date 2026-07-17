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
        for j in range(i + 1, len(points)):
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
    strip = [
        p for p in points_by_x if (p[0] - mid_x) ** 2 < best
    ]  # => points close enough to the midline to possibly beat `best`
    strip.sort(key=lambda p: p[1])  # => sorting the (small) strip by y enables pruning
    for i in range(len(strip)):  # => checks each strip point against its NEAR neighbors
        for j in range(
            i + 1, min(i + 8, len(strip))
        ):  # => a well-known bound: at most 7 useful neighbors in y-sorted order
            best = min(best, squared_distance(strip[i], strip[j]))  # => updates best
    return best  # => the true minimum squared distance across the whole point set


points: list[Point] = [
    (2, 3),
    (12, 30),
    (40, 50),
    (5, 1),
    (12, 10),
    (3, 4),
    (0, 0),
    (20, 20),
]  # => 8 points, deliberately mixing close and far pairs
brute_answer = brute_force_closest_pair(points)  # => O(n^2) ground truth
fast_answer = closest_pair_divide_conquer(points)  # => O(n log n) divide-and-conquer
print(brute_answer)  # => Output: 2
print(fast_answer)  # => Output: 2

assert brute_answer == fast_answer  # => confirms both approaches agree exactly
assert brute_answer == squared_distance(
    (2, 3), (3, 4)
)  # => confirms (2,3)-(3,4) is genuinely the closest pair: dist^2 = 1+1 = 2
print("ex-29 OK")  # => Output: ex-29 OK
