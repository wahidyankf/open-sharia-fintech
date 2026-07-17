-- Example 30: Recursive CTE Graph Cycle.
-- A GRAPH, unlike a tree, can have cycles -- a naive recursive CTE (co-03) over a
-- cyclic route table would loop forever. The fix: carry the visited path in an
-- ARRAY and refuse to revisit any city already in it.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS route CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- route stores directed edges as plain rows -- no PRIMARY KEY, since the same
-- city pair could legitimately appear more than once in a real route network.
CREATE TABLE route(from_city TEXT NOT NULL, to_city TEXT NOT NULL);
                                    -- => a directed edge list -- deliberately contains a CYCLE
INSERT INTO route(from_city, to_city) VALUES
    ('Jakarta', 'Singapore'),
    ('Singapore', 'Bangkok'),
    ('Bangkok', 'Jakarta'),        -- => Bangkok -> Jakarta closes a CYCLE back to the start
    ('Bangkok', 'Hanoi');
                                    -- => without a guard, Jakarta->Singapore->Bangkok->Jakarta->... loops forever

-- The path ARRAY (co-03) accumulates every city visited so far. The recursive
-- term's WHERE clause is the cycle guard: NOT (r.to_city = ANY(path)) refuses to
-- step into a city already on the current path.
-- path is a native Postgres ARRAY column -- ANY(path) and array concatenation
-- (path || r.to_city) are built-in array operators, no separate table needed
-- to track "which cities has this branch of the search already visited".
WITH RECURSIVE reachable AS (
    SELECT from_city AS city, ARRAY[from_city] AS path
    FROM route
    WHERE from_city = 'Jakarta'     -- => anchor: start at Jakarta with a 1-city path
    UNION ALL
-- Each recursive pass explores every outbound edge from the CURRENT frontier
-- of cities -- this is a breadth-first graph walk, not the depth-first walk
-- a recursive function call would perform.
    SELECT r.to_city, reachable.path || r.to_city
    FROM route r
    JOIN reachable ON r.from_city = reachable.city
    WHERE NOT (r.to_city = ANY(reachable.path))
                                    -- => cycle guard: skip any city ALREADY in this path
)
SELECT DISTINCT city FROM reachable ORDER BY city;
                                    -- => Bangkok, Hanoi, Jakarta, Singapore -- every reachable city,
                                    -- => and the query TERMINATES despite the Bangkok->Jakarta cycle
-- Without the cycle guard, PostgreSQL would eventually raise an out-of-memory
-- or statement-timeout error rather than loop truly forever -- but by then it
-- has already done a great deal of wasted, unbounded work.
