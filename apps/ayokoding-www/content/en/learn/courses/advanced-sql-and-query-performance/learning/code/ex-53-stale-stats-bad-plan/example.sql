-- Example 53: Stale Stats, Bad Plan.
-- A SKEWED column (co-25) -- one value overwhelmingly common, another genuinely
-- rare -- is exactly where missing statistics mislead the planner into the WRONG
-- physical strategy, not just an inaccurate row-count estimate (Example 25).
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS skewed_data CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE skewed_data(id INTEGER PRIMARY KEY, category TEXT NOT NULL);
INSERT INTO skewed_data(id, category)
SELECT n, CASE WHEN n % 1000 = 0 THEN 'rare' ELSE 'common' END
FROM generate_series(1, 200000) AS n;
                                    -- => 200,000 rows: 'common' is 99.9%, 'rare' is only 0.1% (200 rows)
CREATE INDEX idx_skewed_category ON skewed_data(category);
                                    -- => the index exists, but NO ANALYZE has run yet on this NEW table

-- BEFORE ANALYZE (co-25): the planner has NO real distribution stats for this
-- table -- it cannot yet know 'rare' is genuinely rare (only 0.1% of rows).
EXPLAIN SELECT * FROM skewed_data WHERE category = 'rare';
                                    -- => rows=1000 estimated (PostgreSQL's generic no-stats guess: 0.5%
                                    -- => of 200,000) -- close-ish, but still a GUESS, not measured data

ANALYZE skewed_data;
                                    -- => ANALYZE (co-25) samples the table -- now it KNOWS the true
                                    -- => 99.9%/0.1% skew via the most-common-values statistics list

-- AFTER ANALYZE: the SAME query, now backed by real, measured selectivity.
EXPLAIN SELECT * FROM skewed_data WHERE category = 'rare';
                                    -- => rows=200 estimated -- matches the TRUE count exactly, because
                                    -- => 'rare' is now a tracked most-common-value with its real frequency
