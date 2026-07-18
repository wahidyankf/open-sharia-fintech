-- Example 40: Composite Index Order.
-- A composite index on (customer_id, product_id) (co-19) is sorted by customer_id
-- FIRST, product_id second -- it can only be searched efficiently starting from its
-- LEFTMOST column. customer_id is seeded HIGH-CARDINALITY on purpose: with a
-- high-cardinality leading column, PostgreSQL 18's B-tree skip scan is not worth it
-- (too many distinct customer_id groups to skip between), so the classic left-most-
-- prefix rule holds cleanly -- see the "Why it matters" note below for the exception.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS order_item CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE order_item(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL);
                                    -- => customer_id: ~100,000 distinct values (HIGH cardinality)
                                    -- => product_id: only 20 distinct values (LOW cardinality)
INSERT INTO order_item(id, customer_id, product_id, quantity)
SELECT n, n, 1 + (n % 20), 1 + (n % 5)
FROM generate_series(1, 100000) AS n;
                                    -- => customer_id = n -- every row has a UNIQUE customer_id

CREATE INDEX idx_order_item_customer_product ON order_item(customer_id, product_id);
ANALYZE order_item;
                                    -- => composite B-tree, sorted by (customer_id, product_id)

-- Query 1: filters on customer_id, the LEADING column -- the index is directly usable.
EXPLAIN SELECT * FROM order_item WHERE customer_id = 50000;
                                    -- => Index Scan using idx_order_item_customer_product -- leftmost prefix used

-- Query 2: filters on product_id ONLY -- customer_id (the leading column) is
-- ABSENT from WHERE. With a high-cardinality leading column, skip scan gains
-- nothing (co-19), so the planner falls back to scanning the table directly.
EXPLAIN SELECT * FROM order_item WHERE product_id = 5;
                                    -- => Seq Scan on order_item -- the composite index is NOT used at all
