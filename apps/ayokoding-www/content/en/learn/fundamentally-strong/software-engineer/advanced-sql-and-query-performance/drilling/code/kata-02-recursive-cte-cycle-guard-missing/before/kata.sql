-- Kata 2 (before): a depth cap keeps this demo finite, but the MISSING cycle
-- guard still lets the walk retrace A -> B -> C -> A forever, wasting every
-- step on nodes already visited instead of reaching D even once.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS edge CASCADE;
CREATE TABLE edge(from_node TEXT NOT NULL, to_node TEXT NOT NULL);
INSERT INTO edge(from_node, to_node) VALUES
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'A'),   -- => closes a cycle: A -> B -> C -> A
    ('A', 'D');   -- => a real, non-cycling branch the walk should also reach

-- intent: walk every path reachable from A, never revisiting a node already on the path.
WITH RECURSIVE walk(node, path, depth) AS (
    SELECT 'A'::TEXT, ARRAY['A']::TEXT[], 1
    UNION ALL
    SELECT e.to_node, w.path || e.to_node, w.depth + 1
    FROM edge e
    JOIN walk w ON e.from_node = w.node
    WHERE w.depth < 6
    -- BUG: no "NOT (e.to_node = ANY(w.path))" guard here -- every recursive step
    -- blindly follows every outgoing edge, including the C -> A edge that revisits
    -- a node already on the path. Only the depth < 6 cap keeps this demo finite.
)
SELECT node, path, depth FROM walk ORDER BY depth, node;
