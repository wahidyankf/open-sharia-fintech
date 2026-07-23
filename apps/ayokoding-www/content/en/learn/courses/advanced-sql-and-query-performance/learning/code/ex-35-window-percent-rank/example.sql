-- Example 35: PERCENT_RANK and CUME_DIST.
-- PERCENT_RANK (co-06) reports each row's relative position as a fraction from 0
-- to 1. CUME_DIST reports the fraction of rows AT OR BELOW the current row's rank.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS employee CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- Five employees, five distinct salaries -- no ties, so every rank is unique
-- and PERCENT_RANK/CUME_DIST land on clean, easy-to-verify fractions.
CREATE TABLE employee(id INTEGER PRIMARY KEY, name TEXT NOT NULL, salary NUMERIC(9,2) NOT NULL);
INSERT INTO employee(id, name, salary) VALUES
    (1, 'Linus',   105000), (2, 'Grace',    99000),
    (3, 'Ada',      95000), (4, 'Alan',     88000),
    (5, 'Barbara',  80000);
                                    -- => 5 employees -- PERCENT_RANK/CUME_DIST both range over [0, 1]

-- PERCENT_RANK() (co-06) = (rank - 1) / (total_rows - 1) -- the LOWEST earner is
-- always 0.0, the HIGHEST is always 1.0. CUME_DIST = rows_at_or_below / total_rows.
-- Both return DOUBLE PRECISION, so ROUND needs an explicit ::numeric cast.
SELECT
    name,
    salary,
-- (rank - 1) / (total_rows - 1) is PERCENT_RANK's own formula -- with 5 rows,
-- each step up in rank moves percent_rank by exactly 1/4 = 0.25.
    ROUND(PERCENT_RANK() OVER (ORDER BY salary)::numeric, 3) AS percent_rank,
-- CUME_DIST's denominator is total_rows, not total_rows - 1 -- that's why the
-- LOWEST earner's cume_dist (0.200 = 1/5) is never 0.0, unlike percent_rank.
    ROUND(CUME_DIST()    OVER (ORDER BY salary)::numeric, 3) AS cume_dist
FROM employee
ORDER BY salary;
                                    -- => Barbara (lowest): percent_rank 0.000, cume_dist 0.200 (1 of 5 rows)
                                    -- => Linus (highest): percent_rank 1.000, cume_dist 1.000 (all 5 rows)
