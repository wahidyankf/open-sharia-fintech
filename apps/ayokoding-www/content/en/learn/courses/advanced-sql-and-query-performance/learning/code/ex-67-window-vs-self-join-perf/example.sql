-- Example 67: Window vs Self-Join Performance.
-- A running total can be computed TWO ways: a window function (co-04) in one pass,
-- or a classic self-join summing all PRECEDING rows -- same logical result, very
-- different cost, because the self-join reprocesses O(n^2) row pairs (co-24).
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS daily_revenue CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- Revenue oscillates between 100 and 149 via the (n % 50) trick -- the exact
-- values do not matter here, only that 3,000 distinct rows exist to sum over.
CREATE TABLE daily_revenue(day_number INTEGER PRIMARY KEY, revenue NUMERIC(10,2) NOT NULL);
INSERT INTO daily_revenue(day_number, revenue)
SELECT n, (100 + (n % 50))::NUMERIC FROM generate_series(1, 3000) AS n;
                                    -- => 3,000 rows -- large enough for the O(n^2) self-join to hurt

-- Approach 1: window function (co-04) -- ONE pass over the data, O(n) or O(n log n).
EXPLAIN (ANALYZE, TIMING OFF)
SELECT day_number, revenue,
    -- The explicit ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW frame is
    -- exactly what makes this a running total -- Postgres needs only ONE sorted
    -- pass, accumulating the sum as it walks through in day_number order.
    SUM(revenue) OVER (ORDER BY day_number ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM daily_revenue;
                                    -- => a single WindowAgg node over one sorted scan

-- Approach 2: self-join (co-24) -- for EVERY row, join to ALL rows with a smaller
-- day_number and SUM them -- classic pre-window-function SQL, O(n^2) row comparisons.
EXPLAIN (ANALYZE, TIMING OFF)
SELECT a.day_number, a.revenue, SUM(b.revenue) AS running_total
FROM daily_revenue a
-- Non-equi JOIN condition (<=, not =) -- this is what forces the planner into
-- a quadratic-shaped comparison instead of a simple hash lookup per row.
JOIN daily_revenue b ON b.day_number <= a.day_number
GROUP BY a.day_number, a.revenue
ORDER BY a.day_number;
                                    -- => a nested loop or hash join comparing EVERY pair of rows
-- At 3,000 rows this self-join compares roughly 4.5 million row pairs -- the
-- EXPLAIN ANALYZE timing above makes the real cost of that O(n^2) growth visible.
