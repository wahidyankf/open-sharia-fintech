-- Example 79: EXPLAIN Buffers, I/O Tuning.
-- "Buffers" (co-23) counts how many 8KB pages a query TOUCHES -- an unindexed
-- filter on a big table touches EVERY page (a full Seq Scan); adding the right
-- index (co-18) can shrink that count from thousands of pages to a handful.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS support_ticket CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE support_ticket(id INTEGER PRIMARY KEY, ticket_number TEXT NOT NULL, status TEXT NOT NULL, body TEXT NOT NULL);
INSERT INTO support_ticket(id, ticket_number, status, body)
SELECT n, 'TKT-' || LPAD(n::TEXT, 8, '0'),
    CASE WHEN n = 250000 THEN 'urgent' ELSE 'normal' END,
    repeat('lorem ipsum dolor sit amet ', 10)
                                    -- => a wide TEXT body column -- inflates page count realistically,
                                    -- => and exactly ONE row out of 500,000 has status = 'urgent'
FROM generate_series(1, 500000) AS n;
-- VACUUM here builds the visibility map before ANALYZE runs -- consistent
-- with the pattern used in every other Buffers/EXPLAIN example in this topic.
VACUUM support_ticket;
ANALYZE support_ticket;

-- BEFORE the index: finding the one 'urgent' ticket means touching EVERY page.
EXPLAIN (ANALYZE, TIMING OFF) SELECT id FROM support_ticket WHERE status = 'urgent';
                                    -- => Seq Scan -- Buffers: shared hit=N, where N is roughly the
                                    -- => table's FULL page count -- every page gets touched and filtered

-- A plain B-tree index on status is enough here -- only 2 distinct values
-- exist ('urgent', 'normal'), but their extreme skew (1 vs 499,999 rows)
-- is exactly what makes an index dramatically cheaper than a full scan.
CREATE INDEX idx_support_ticket_status ON support_ticket(status);
ANALYZE support_ticket;

-- AFTER the index: the SAME query, dramatically fewer pages touched.
EXPLAIN (ANALYZE, TIMING OFF) SELECT id FROM support_ticket WHERE status = 'urgent';
                                    -- => Bitmap Heap Scan / Bitmap Index Scan -- Buffers drops sharply,
                                    -- => because the index directly points at the ONE matching row's page
