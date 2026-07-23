-- Kata 9 (before): a partial index whose predicate does NOT syntactically match
-- the query's WHERE clause is silently unusable -- no error, just a Seq Scan.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS ticket CASCADE;
CREATE TABLE ticket(id INTEGER PRIMARY KEY, status TEXT NOT NULL);
INSERT INTO ticket(id, status)
SELECT n, CASE WHEN n % 200 = 0 THEN 'open' ELSE 'closed' END
FROM generate_series(1, 100000) AS n;
-- a partial index over ONLY the 'open' tickets -- most tickets are 'closed'
-- and never need this index at all.
CREATE INDEX idx_ticket_open ON ticket(id) WHERE status = 'open';
ANALYZE ticket;

-- BUG: the query's predicate is status != 'closed', which is LOGICALLY the
-- same set of rows as status = 'open' here, but the planner only matches a
-- partial index's predicate SYNTACTICALLY -- it does not prove the two forms
-- are equivalent, so the index below is silently never considered.
EXPLAIN SELECT * FROM ticket WHERE status != 'closed';
