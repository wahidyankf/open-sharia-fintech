-- Example 65: Recursive CTE, Shortest Path.
-- A recursive CTE (co-03) can explore EVERY simple path through a weighted graph
-- and pick the cheapest -- a small, teaching-scale version of what pathfinding
-- algorithms like Dijkstra's compute more efficiently at large scale.
-- This graph is DIRECTED (from_city -> to_city is one-way) and has NO edge
-- back from D to anywhere -- D is a pure sink, which is why the guard below
-- only needs to prevent CYCLES, not worry about an unbounded search space.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS road_edge CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- distance_km is a plain INTEGER, not NUMERIC -- road distances here are whole
-- kilometers, so no fractional-money precision concerns like Example 1's prices.
CREATE TABLE road_edge(from_city TEXT NOT NULL, to_city TEXT NOT NULL, distance_km INTEGER NOT NULL);
-- Five edges define a small graph with a deliberate trap: the DIRECT A->B edge
-- (weight 10) looks obviously cheap, but the two-hop A->C->B route (1+1=2) is
-- far cheaper -- exactly the kind of case a naive greedy shortest-path guess gets wrong.
INSERT INTO road_edge(from_city, to_city, distance_km) VALUES
    ('A', 'B', 10),                -- => direct A->B looks cheap-ish at first glance
    ('A', 'C', 1),
    ('C', 'B', 1),                 -- => A->C->B totals 2, MUCH cheaper than direct A->B
    ('B', 'D', 5),
    ('C', 'D', 20);                -- => A->C->D totals 21 -- a trap for a "greedy" reader

-- visited is an ARRAY column threaded through every recursive iteration -- it
-- is what lets the WHERE clause below distinguish a legitimate longer path
-- from an infinite loop back through an already-visited city.
WITH RECURSIVE search_path(city, total_distance, visited) AS (
    SELECT 'A'::TEXT, 0, ARRAY['A']::TEXT[]
                                    -- => anchor (co-03): start at A with distance 0
    UNION ALL
    -- Every recursive iteration JOINS the current frontier of paths against
    -- EVERY outgoing edge from the path's current city -- this is what makes
    -- the search explore ALL paths, not just one greedy route.
    SELECT e.to_city, sp.total_distance + e.distance_km, sp.visited || e.to_city
    FROM search_path sp
    JOIN road_edge e ON e.from_city = sp.city
    WHERE NOT e.to_city = ANY(sp.visited)
                                    -- => cycle guard (co-03): ARRAY path tracking, not just depth --
                                    -- => needed because this graph has A->C->B->D AND A->B directly,
                                    -- => so a naive depth-limit guard could still loop on other graphs
)
-- ORDER BY total_distance LIMIT 1 over the FULL set of explored paths to D is
-- what actually finds the cheapest route -- this brute-force approach works
-- fine at this graph's tiny scale but does not scale the way a real Dijkstra
-- implementation (which prunes as it goes) would on a large graph.
SELECT city, total_distance, visited
FROM search_path
WHERE city = 'D'
ORDER BY total_distance
LIMIT 1;
                                    -- => picks the CHEAPEST of ALL explored paths to D, not the FIRST found
-- The returned `visited` array is the actual path taken -- A, C, B, D -- proving
-- the recursive search found the 2+1+5=8 route, not the naive-looking 10+5=15.
