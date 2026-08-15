"""Original runnable reference routines for Coding Interview examples.

Each function makes a course invariant concrete. They are intentionally small:
the learning pages teach the spoken reasoning, while this module gives that
reasoning a deterministic executable check.
"""

from __future__ import annotations

from collections import Counter, deque
import heapq


def two_sum_indices(values: list[int], target: int) -> tuple[int, int] | None:
    """Return two distinct indices in expected O(n) time and O(n) space (ex-05)."""
    seen: dict[int, int] = {}
    for index, value in enumerate(values):
        complement = target - value
        if complement in seen:
            return (seen[complement], index)
        seen[value] = index
    return None


def longest_unique(text: str) -> int:
    """Return longest duplicate-free substring length in O(n) time (ex-09)."""
    left = 0
    last_seen: dict[str, int] = {}
    best = 0
    for right, character in enumerate(text):
        if character in last_seen and last_seen[character] >= left:
            left = last_seen[character] + 1
        last_seen[character] = right
        best = max(best, right - left + 1)
    return best


def first_last(values: list[int], target: int) -> tuple[int, int]:
    """Find target boundaries with two binary searches (ex-11)."""

    def bound(find_left: bool) -> int:
        low, high, answer = 0, len(values) - 1, -1
        while low <= high:
            middle = (low + high) // 2
            if values[middle] == target:
                answer = middle
                if find_left:
                    high = middle - 1
                else:
                    low = middle + 1
            elif values[middle] < target:
                low = middle + 1
            else:
                high = middle - 1
        return answer

    return (bound(True), bound(False))


def shortest_grid_path(grid: list[list[int]]) -> int:
    """Minimum 4-neighbour hops through zero cells, or -1 (ex-19)."""
    if not grid or not grid[0] or grid[0][0] or grid[-1][-1]:
        return -1
    rows, columns = len(grid), len(grid[0])
    queue: deque[tuple[int, int, int]] = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while queue:
        row, column, distance = queue.popleft()
        if (row, column) == (rows - 1, columns - 1):
            return distance
        for d_row, d_column in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row, next_column = row + d_row, column + d_column
            if (
                0 <= next_row < rows
                and 0 <= next_column < columns
                and not grid[next_row][next_column]
                and (next_row, next_column) not in seen
            ):
                seen.add((next_row, next_column))
                queue.append((next_row, next_column, distance + 1))
    return -1


def min_coin_count(coins: list[int], amount: int) -> int:
    """Minimum coins via tabulation, reporting -1 when unreachable (ex-28)."""
    if amount < 0:
        return -1
    best = [amount + 1] * (amount + 1)
    best[0] = 0
    for subtotal in range(1, amount + 1):
        for coin in coins:
            if coin <= subtotal:
                best[subtotal] = min(best[subtotal], best[subtotal - coin] + 1)
    return -1 if best[amount] == amount + 1 else best[amount]


def schedule(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Choose a maximum compatible set by earliest finish (ex-30)."""
    result: list[tuple[int, int]] = []
    finish = float("-inf")
    for interval in sorted(intervals, key=lambda item: item[1]):
        if interval[0] >= finish:
            result.append(interval)
            finish = interval[1]
    return result


def top_k(values: list[int], k: int) -> list[int]:
    """Return largest k values using O(k) heap space (ex-32)."""
    if k <= 0:
        return []
    heap: list[int] = []
    for value in values:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)
    return sorted(heap, reverse=True)


def next_greater(values: list[int]) -> list[int]:
    """Return first later greater value, or -1, using a monotonic stack (ex-35)."""
    answers = [-1] * len(values)
    unresolved: list[int] = []
    for index, value in enumerate(values):
        while unresolved and values[unresolved[-1]] < value:
            answers[unresolved.pop()] = value
        unresolved.append(index)
    return answers


def min_cover(text: str, target: str) -> str:
    """Minimum covering substring using count-preserving sliding window (ex-45)."""
    if not target:
        return ""
    required = Counter(target)
    window: Counter[str] = Counter()
    formed = 0
    left = 0
    best: tuple[int, int] | None = None
    for right, character in enumerate(text):
        window[character] += 1
        if character in required and window[character] == required[character]:
            formed += 1
        while formed == len(required):
            if best is None or right - left < best[1] - best[0]:
                best = (left, right)
            removed = text[left]
            window[removed] -= 1
            if removed in required and window[removed] < required[removed]:
                formed -= 1
            left += 1
    return "" if best is None else text[best[0] : best[1] + 1]
