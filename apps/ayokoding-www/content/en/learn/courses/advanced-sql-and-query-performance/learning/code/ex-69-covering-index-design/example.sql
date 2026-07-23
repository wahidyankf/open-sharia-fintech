-- Example 69: Covering Index Design.
-- The hot query below is called on EVERY page load: "give me this order's status
-- and total for display." Designing a covering index (co-19) with INCLUDE columns
-- lets it be answered from the index alone -- no heap access needed at all.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS storefront_order CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- order_number is what customers and support staff search by -- status and
-- total are the two columns the hot page-load query always needs alongside it.
CREATE TABLE storefront_order(
    id INTEGER PRIMARY KEY, order_number TEXT NOT NULL, status TEXT NOT NULL, total NUMERIC(10,2) NOT NULL
);
-- LPAD zero-pads the order number to a fixed 8-digit width -- a realistic
-- order-number format, and guarantees each value is unique across all 300K rows.
INSERT INTO storefront_order(id, order_number, status, total)
SELECT n, 'ORD-' || LPAD(n::TEXT, 8, '0'),
    (ARRAY['pending', 'shipped', 'delivered'])[1 + (n % 3)], (10 + (n % 500))::NUMERIC
FROM generate_series(1, 300000) AS n;
                                    -- => 300,000 rows -- the hot query is "look up by order_number"
VACUUM storefront_order;
                                    -- => builds the visibility map -- REQUIRED for Index Only Scan to
                                    -- => trust the index without visiting the heap (same as Example 41)

-- BASELINE: an ORDINARY (non-covering) index -- an equality lookup on order_number
-- finds the row fast, but status/total still require a SEPARATE heap fetch.
CREATE INDEX idx_order_number_plain ON storefront_order(order_number);
ANALYZE storefront_order;
EXPLAIN (ANALYZE, TIMING OFF)
SELECT status, total FROM storefront_order WHERE order_number = 'ORD-00150000';
                                    -- => Index Scan (NOT "Index Only") -- status/total live in the heap,
                                    -- => outside the plain index, so a heap fetch is still required

DROP INDEX idx_order_number_plain;

-- THE FIX (co-19): a covering index -- order_number is the SEARCH key, status and
-- total ride along as INCLUDE columns, physically stored IN the index itself.
-- INCLUDE columns are NOT part of the B-tree's sort key -- they cannot be used to
-- accelerate a WHERE or ORDER BY, only to satisfy a SELECT list without a heap trip.
CREATE INDEX idx_order_number_covering ON storefront_order(order_number) INCLUDE (status, total);
ANALYZE storefront_order;
EXPLAIN (ANALYZE, TIMING OFF)
SELECT status, total FROM storefront_order WHERE order_number = 'ORD-00150000';
                                    -- => Index Only Scan -- EVERY column the query needs (order_number
                                    -- => for the search, status+total for the output) lives IN the index
-- The trade-off: a covering index is LARGER on disk and slightly slower to
-- write to than a plain one -- worth it only for genuinely hot, narrow queries.
