-- Kata 2 (after): the cycle guard sits in the RECURSIVE term, where it is
-- actually evaluated on every step -- the walk now terminates on its own.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS edge CASCADE;
CREATE TABLE edge(from_node TEXT NOT NULL, to_node TEXT NOT NULL);
INSERT INTO edge(from_node, to_node) VALUES
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'A'),
    ('A', 'D');

WITH RECURSIVE walk(node, path, depth) AS (
    SELECT 'A'::TEXT, ARRAY['A']::TEXT[], 1
    UNION ALL
    SELECT e.to_node, w.path || e.to_node, w.depth + 1
    FROM edge e
    JOIN walk w ON e.from_node = w.node
    -- THE FIX: NOT (e.to_node = ANY(w.path)) skips any edge leading BACK to a
    -- node already on this path -- the C -> A edge is now excluded once A is
    -- already visited, so the recursion terminates on its own, no depth cap needed.
    WHERE NOT (e.to_node = ANY(w.path))
)
SELECT node, path, depth FROM walk ORDER BY depth, node;
