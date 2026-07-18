-- Example 80: Planner Cost Constants.
-- random_page_cost (co-24) tells the planner how expensive a RANDOM disk page
-- fetch is relative to a SEQUENTIAL one -- its default (4.0) models spinning disks;
-- lowering it (modeling SSDs) can flip the planner's own choice of physical plan.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS product_catalog CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE product_catalog(id INTEGER PRIMARY KEY, category_id INTEGER NOT NULL, name TEXT NOT NULL);
INSERT INTO product_catalog(id, category_id, name)
SELECT n, 1 + (n % 20), 'Product ' || n FROM generate_series(1, 500000) AS n;
                                    -- => 500,000 rows, 20 categories -- category_id=3 is ~5% of rows
CREATE INDEX idx_product_catalog_category ON product_catalog(category_id);
ANALYZE product_catalog;

SHOW random_page_cost;
                                    -- => PostgreSQL's default: 4 -- models a spinning disk, where a
                                    -- => random seek is modeled as 4x costlier than sequential access

-- Bitmap Heap Scan sits cost-wise BETWEEN a plain Seq Scan and a plain Index Scan,
-- so it wins either way and would hide the flip -- disable it for a CLEAN two-way
-- comparison (teaching-only, exactly like Examples 49-51 disabling other join types).
SET enable_bitmapscan = off;

-- AT THE DEFAULT (4): for a ~5%-selective filter, the planner judges a plain Index
-- Scan's random-access pattern too costly and prefers a Seq Scan instead (co-24).
EXPLAIN SELECT id FROM product_catalog WHERE category_id = 3;
                                    -- => Parallel Seq Scan chosen -- cost=1000.00..9277.47

SET random_page_cost = 1.1;
                                    -- => 1.1 models FAST SSD/NVMe storage, where random access is
                                    -- => nearly as cheap as sequential -- realistic for most production
                                    -- => databases today, which is why many teams tune this DOWN from 4

-- SAME query, SAME data, SAME index -- ONLY the cost model changed.
EXPLAIN SELECT id FROM product_catalog WHERE category_id = 3;
                                    -- => the planner FLIPS to a plain Index Scan (cost=0.42..3955.47) --
                                    -- => nothing about the query, the data, or the index changed; only
                                    -- => the planner's belief about random I/O cost on THIS hardware did
