"""Five original capstone references, one for each timed mock-round pattern."""

from __future__ import annotations

import heapq
from collections import deque


def pair_indices(values: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for index, value in enumerate(values):
        if target - value in seen:
            return (seen[target - value], index)
        seen[value] = index
    return None


def longest_sum_at_most(values: list[int], limit: int) -> int:
    left = total = best = 0
    for right, value in enumerate(values):
        total += value
        while total > limit and left <= right:
            total -= values[left]
            left += 1
        best = max(best, right - left + 1)
    return best


def count_islands(grid: list[list[int]]) -> int:
    if not grid:
        return 0
    rows, columns, count = len(grid), len(grid[0]), 0
    seen: set[tuple[int, int]] = set()
    for row in range(rows):
        for column in range(columns):
            if grid[row][column] or (row, column) in seen:
                continue
            count += 1
            queue: deque[tuple[int, int]] = deque([(row, column)])
            seen.add((row, column))
            while queue:
                current_row, current_column = queue.popleft()
                for d_row, d_column in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    next_row, next_column = (
                        current_row + d_row,
                        current_column + d_column,
                    )
                    if (
                        0 <= next_row < rows
                        and 0 <= next_column < columns
                        and not grid[next_row][next_column]
                        and (next_row, next_column) not in seen
                    ):
                        seen.add((next_row, next_column))
                        queue.append((next_row, next_column))
    return count


def select_meetings(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    accepted: list[tuple[int, int]] = []
    finish = float("-inf")
    for interval in sorted(intervals, key=lambda item: item[1]):
        if interval[0] >= finish:
            accepted.append(interval)
            finish = interval[1]
    return accepted


def streaming_top_k(values: list[int], k: int) -> list[int]:
    heap: list[int] = []
    for value in values:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif k and value > heap[0]:
            heapq.heapreplace(heap, value)
    return sorted(heap, reverse=True)
