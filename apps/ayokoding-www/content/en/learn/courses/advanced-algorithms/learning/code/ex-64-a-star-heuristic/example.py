"""Example 64: A* Search -- Same Cost as Dijkstra, Fewer Nodes Expanded."""

# A* (co-19) is Dijkstra plus a HEURISTIC: it orders the frontier by g+h
# (cost-so-far plus estimated cost-to-goal) instead of g alone. An ADMISSIBLE
# heuristic (never overestimates -- Manhattan distance on a 4-directional
# grid) guarantees A* still finds the OPTIMAL path, while expanding fewer
# nodes than Dijkstra, which has no sense of "which direction is promising."
import heapq  # => the min-heap priority queue both searches use to pick a frontier cell

Cell = tuple[int, int]  # => a grid position (row, col)


def neighbors(cell: Cell, rows: int, cols: int) -> list[Cell]:  # => 4-directional moves
    r, c = cell  # => the cell's own row/column
    candidates = [  # => opens the four-direction candidate list
        (r + 1, c),  # => down
        (r - 1, c),  # => up
        (r, c + 1),  # => right
        (r, c - 1),  # => left
    ]  # => down/up/right/left
    return [  # => opens the in-bounds filter
        (nr, nc)  # => a candidate cell that survives the bounds check
        for nr, nc in candidates  # => checks every one of the 4 candidate moves
        if 0 <= nr < rows and 0 <= nc < cols  # => in-bounds only
    ]  # => stays within the grid's bounds


def manhattan(
    a: Cell,  # => the first cell being measured
    b: Cell,  # => the two cells to measure between
) -> int:  # => the ADMISSIBLE heuristic: never overestimates
    return abs(a[0] - b[0]) + abs(  # => row distance plus (opens) column distance
        a[1] - b[1]  # => the absolute column distance
    )  # => a lower bound on any grid path's cost


def dijkstra_grid(  # => baseline: orders the frontier by cost-so-far (g) alone
    rows: int,  # => the grid's row count
    cols: int,  # => the grid's column count
    start: Cell,  # => the search's origin cell
    goal: Cell,  # => grid size, start cell, goal cell
) -> tuple[int, int]:  # => (path cost, nodes expanded)
    dist: dict[Cell, int] = {start: 0}  # => cost-so-far to reach each visited cell
    heap: list[tuple[int, Cell]] = [(0, start)]  # => (g, cell) -- ordered by g alone
    expanded = 0  # => counts FINALIZED node expansions
    visited: set[Cell] = set()  # => cells whose shortest cost is already finalized
    while heap:  # => keeps going until the goal is reached or the heap is empty
        g, cell = heapq.heappop(heap)  # => pops the cheapest-so-far unfinished cell
        if cell in visited:  # => a stale heap entry -- already finalized more cheaply
            continue  # => skip it, no work to redo
        visited.add(cell)  # => this cell's shortest cost is now final
        expanded += 1  # => one more node finalized
        if cell == goal:  # => reached the goal -- its distance is now final
            return g, expanded  # => the optimal cost, plus how much work it took
        for nxt in neighbors(cell, rows, cols):  # => tries every 4-directional neighbor
            new_g = g + 1  # => every grid step costs 1
            if new_g < dist.get(
                nxt,  # => this neighbor's cell key
                float("inf"),  # => treats an unvisited neighbor as infinitely far
            ):  # => a strictly cheaper path was found
                dist[nxt] = new_g  # => records the improved cost
                heapq.heappush(heap, (new_g, nxt))  # => queues it, ordered by g alone
    return -1, expanded  # => unreachable (never happens on a full grid)


def a_star_grid(  # => same search, but orders the frontier by g+h (estimated total cost)
    rows: int,  # => the grid's row count
    cols: int,  # => the grid's column count
    start: Cell,  # => the search's origin cell
    goal: Cell,  # => grid size, start cell, goal cell
) -> tuple[int, int]:  # => (path cost, nodes expanded)
    g_score: dict[Cell, int] = {start: 0}  # => cost-so-far to reach each visited cell
    heap: list[tuple[int, Cell]] = [
        (manhattan(start, goal), start)  # => f = h at the start, since g is 0
    ]  # => (f = g+h, cell) -- ordered by the ESTIMATED total cost
    expanded = 0  # => counts FINALIZED node expansions
    visited: set[Cell] = set()  # => cells whose shortest cost is already finalized
    while heap:  # => keeps going until the goal is reached or the heap is empty
        _, cell = heapq.heappop(heap)  # => pops the most-promising unfinished cell
        if cell in visited:  # => a stale heap entry -- already finalized more cheaply
            continue  # => skip it, no work to redo
        visited.add(cell)  # => this cell's shortest cost is now final
        expanded += 1  # => one more node finalized
        if cell == goal:  # => reached the goal -- its cost is now final and OPTIMAL
            return g_score[
                cell  # => the goal's own finalized cost-so-far
            ], expanded  # => the optimal cost, plus how much work it took
        for nxt in neighbors(cell, rows, cols):  # => tries every 4-directional neighbor
            new_g = g_score[cell] + 1  # => every grid step costs 1
            if new_g < g_score.get(
                nxt,  # => this neighbor's cell key
                float("inf"),  # => treats an unvisited neighbor as infinitely far
            ):  # => a strictly cheaper path was found
                g_score[nxt] = new_g  # => records the improved cost-so-far
                heapq.heappush(  # => the heap may end up holding stale entries too
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
dijkstra_cost, dijkstra_expanded = dijkstra_grid(  # => opens the baseline run
    rows,  # => the grid's row count
    cols,  # => the grid's column count
    start,  # => the search's origin cell
    goal,  # => the same grid, start, and goal as A* will use
)  # => baseline run
a_star_cost, a_star_expanded = a_star_grid(  # => opens the heuristic-guided run
    rows,  # => the same row count as Dijkstra's run above
    cols,  # => the same column count as Dijkstra's run above
    start,  # => the same origin cell as Dijkstra's run above
    goal,  # => the same grid, start, and goal Dijkstra already used
)  # => heuristic-guided run
print(dijkstra_cost == a_star_cost)  # => Output: True
print(a_star_expanded < dijkstra_expanded)  # => Output: True

assert dijkstra_cost == a_star_cost  # => confirms BOTH found the same optimal cost
assert dijkstra_cost == 6  # => the Manhattan distance from (15,15) to (18,18): 3+3
assert (  # => opens the A*-expands-fewer-nodes check
    a_star_expanded < dijkstra_expanded
)  # => confirms A*'s heuristic genuinely reduces expansions
print("ex-64 OK")  # => Output: ex-64 OK
