-- Example 51: EXPLAIN Merge Join.
-- A Merge Join (co-24) walks BOTH sides in sorted order simultaneously, like
-- merging two sorted lists -- cheap when both sides are ALREADY sorted (via an
-- index, as here) or when sorting them first is still cheaper than a hash table.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS order_row, customer CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- Both sides get an index on the join column here -- customer via its PRIMARY
-- KEY, order_row via an explicit CREATE INDEX -- giving Merge Join two
-- already-sorted inputs to walk in lockstep.
CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
INSERT INTO customer(id, name) SELECT n, 'Customer ' || n FROM generate_series(1, 20000) AS n;
                                    -- => 20,000 customers, PRIMARY KEY already sorts by id
CREATE TABLE order_row(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL);
INSERT INTO order_row(id, customer_id)
SELECT n, 1 + (n % 20000) FROM generate_series(1, 100000) AS n;
                                    -- => 100,000 orders -- an index on customer_id gives a SECOND sorted input
CREATE INDEX idx_order_customer_id ON order_row(customer_id);
ANALYZE customer;
ANALYZE order_row;

-- Force Merge Join specifically so the plan is deterministic -- production code
-- should never disable other join strategies; this is teaching-only.
-- Disabling the other two strategies again forces a deterministic plan for
-- this teaching example -- Merge Join would otherwise have to compete against
-- Nested Loop's indexed lookups and Hash Join's build-then-probe approach.
SET enable_nestloop = off;
SET enable_hashjoin = off;

EXPLAIN SELECT c.name, COUNT(*) AS order_count
FROM customer c
JOIN order_row o ON o.customer_id = c.id
GROUP BY c.name;
                                    -- => Merge Join: BOTH inputs arrive sorted by the join key already --
                                    -- => customer via its PRIMARY KEY index, order_row via idx_order_customer_id
                                    -- => no separate hash table, no per-row index probe -- a single merged pass
