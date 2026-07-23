-- Kata 9 (after): rewriting the WHERE clause to match the index's predicate
-- syntax lets the planner prove the index applies.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS ticket CASCADE;
CREATE TABLE ticket(id INTEGER PRIMARY KEY, status TEXT NOT NULL);
INSERT INTO ticket(id, status)
SELECT n, CASE WHEN n % 200 = 0 THEN 'open' ELSE 'closed' END
FROM generate_series(1, 100000) AS n;
CREATE INDEX idx_ticket_open ON ticket(id) WHERE status = 'open';
ANALYZE ticket;

-- THE FIX: status = 'open' (co-21) matches the index's own predicate text
-- exactly -- the planner can now prove every row this index covers satisfies
-- the query's WHERE clause too, so it uses the much smaller partial index.
EXPLAIN SELECT * FROM ticket WHERE status = 'open';
