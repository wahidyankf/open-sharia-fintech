"""Example 64: A* Search -- Same Cost as Dijkstra, Fewer Nodes Expanded."""

# A* (co-19) is Dijkstra plus a HEURISTIC: it orders the frontier by g+h
# (cost-so-far plus estimated cost-to-goal) instead of g alone. An ADMISSIBLE
# heuristic (never overestimates -- Manhattan distance on a 4-directional
# grid) guarantees A* still finds the OPTIMAL path, while expanding fewer
# nodes than Dijkstra, which has no sense of "which direction is promising."
import heapq

Cell = tuple[int, int]  # => a grid position (row, col)


def neighbors(cell: Cell, rows: int, cols: int) -> list[Cell]:  # => 4-directional moves
    r, c = cell
    candidates = [
        (r + 1, c),
        (r - 1, c),
        (r, c + 1),
        (r, c - 1),
    ]  # => down/up/right/left
    return [
        (nr, nc) for nr, nc in candidates if 0 <= nr < rows and 0 <= nc < cols
    ]  # => stays within the grid's bounds


def manhattan(
    a: Cell, b: Cell
) -> int:  # => the ADMISSIBLE heuristic: never overestimates
    return abs(a[0] - b[0]) + abs(
        a[1] - b[1]
    )  # => a lower bound on any grid path's cost


def dijkstra_grid(
    rows: int, cols: int, start: Cell, goal: Cell
) -> tuple[int, int]:  # => (path cost, nodes expanded)
    dist: dict[Cell, int] = {start: 0}  # => cost-so-far to reach each visited cell
    heap: list[tuple[int, Cell]] = [(0, start)]  # => (g, cell) -- ordered by g alone
    expanded = 0  # => counts FINALIZED node expansions
    visited: set[Cell] = set()
    while heap:
        g, cell = heapq.heappop(heap)
        if cell in visited:
            continue
        visited.add(cell)
        expanded += 1  # => one more node finalized
        if cell == goal:  # => reached the goal -- its distance is now final
            return g, expanded
        for nxt in neighbors(cell, rows, cols):
            new_g = g + 1  # => every grid step costs 1
            if new_g < dist.get(nxt, float("inf")):
                dist[nxt] = new_g
                heapq.heappush(heap, (new_g, nxt))
    return -1, expanded  # => unreachable (never happens on a full grid)


def a_star_grid(
    rows: int, cols: int, start: Cell, goal: Cell
) -> tuple[int, int]:  # => (path cost, nodes expanded)
    g_score: dict[Cell, int] = {start: 0}  # => cost-so-far to reach each visited cell
    heap: list[tuple[int, Cell]] = [
        (manhattan(start, goal), start)
    ]  # => (f = g+h, cell) -- ordered by the ESTIMATED total cost
    expanded = 0  # => counts FINALIZED node expansions
    visited: set[Cell] = set()
    while heap:
        _, cell = heapq.heappop(heap)
        if cell in visited:
            continue
        visited.add(cell)
        expanded += 1  # => one more node finalized
        if cell == goal:  # => reached the goal -- its cost is now final and OPTIMAL
            return g_score[cell], expanded
        for nxt in neighbors(cell, rows, cols):
            new_g = g_score[cell] + 1  # => every grid step costs 1
            if new_g < g_score.get(nxt, float("inf")):
                g_score[nxt] = new_g
                heapq.heappush(
                    heap, (new_g + manhattan(nxt, goal), nxt)
                )  # => f = g + h steers the search TOWARD the goal
    return -1, expanded  # => unreachable (never happens on a full grid)


# A goal near the CENTER of a large grid (not a far corner) is what actually
# lets the heuristic discriminate: Dijkstra, blind to direction, must expand
# every cell within Manhattan-distance-6 of start -- including cells pointing
# entirely AWAY from goal. A*'s heuristic confines expansion to the much
# smaller rectangle of cells that could plausibly lie on a shortest path.
rows, cols = 30, 30  # => a large grid -- plenty of room for goal-irrelevant cells
start, goal = (15, 15), (18, 18)  # => goal is near the center, not a far corner
dijkstra_cost, dijkstra_expanded = dijkstra_grid(rows, cols, start, goal)
a_star_cost, a_star_expanded = a_star_grid(rows, cols, start, goal)
print(dijkstra_cost == a_star_cost)  # => Output: True
print(a_star_expanded < dijkstra_expanded)  # => Output: True

assert dijkstra_cost == a_star_cost  # => confirms BOTH found the same optimal cost
assert dijkstra_cost == 6  # => the Manhattan distance from (15,15) to (18,18): 3+3
assert (
    a_star_expanded < dijkstra_expanded
)  # => confirms A*'s heuristic genuinely reduces expansions
print("ex-64 OK")  # => Output: ex-64 OK
