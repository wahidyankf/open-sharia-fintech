-- Example 36: Top-N per Group.
-- ROW_NUMBER() PARTITION BY ... (co-06) numbers rows WITHIN each group -- filtering
-- WHERE rn <= N in an outer query is the standard "top N per group" pattern.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS employee CASCADE;
-- Resetting the table first guarantees exactly 6 rows -- 3 per department --
-- regardless of what any earlier example left behind.

-- => resets state -- this example is fully self-contained
-- Same employee shape as Example 9, now with a second department seeded so
-- "top N PER group" has two independent groups to demonstrate against.
CREATE TABLE employee (
-- id is unused in either the CTE or the final SELECT -- it exists purely
-- as the table's primary key, not because this query needs it.
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
-- dept is the PARTITION BY key -- every distinct value becomes its own
-- independent numbering group, however many departments end up existing.
  dept TEXT NOT NULL,
-- Same money-safe NUMERIC precision convention used throughout this topic's
-- salary columns.
  salary NUMERIC(9, 2) NOT NULL
);

-- 3 rows per department, salaries all distinct within each dept -- clean ranks
-- with no ties to complicate which 2 rows "top 2" should keep.
INSERT INTO
  employee (id, name, dept, salary)
VALUES
  (1, 'Linus', 'Engineering', 105000),
  (2, 'Ada', 'Engineering', 95000),
  (3, 'Barbara', 'Engineering', 88000),
  (4, 'Grace', 'Data', 99000),
  (5, 'Alan', 'Data', 91000),
  (6, 'Edsger', 'Data', 85000);

-- => 3 Engineering, 3 Data -- top-2 per dept below excludes 2 rows total
-- ROW_NUMBER() CANNOT appear in a WHERE clause directly (window functions run
-- AFTER WHERE) -- wrap it in a subquery/CTE, then filter the OUTER query (co-06).
-- This is the SAME problem Example 10 introduced for a single, ungrouped rank
-- -- Top-N per group is that same numbering trick with PARTITION BY layered on.
WITH
-- ranked is a plain (non-recursive) CTE -- exactly the Example 4 pattern,
-- just carrying a window function's output through to the outer query.
  ranked AS (
    SELECT
-- name, dept, and salary all ride through the CTE untouched -- ranked simply
-- adds rn alongside the original columns, it does not transform them.
      name,
      dept,
      salary,
-- PARTITION BY dept resets the numbering back to 1 at the start of EACH
-- department -- without it, rn would count 1 through 6 across the whole table,
-- and "rn <= 2" would keep only the 2 single highest earners company-wide.
      ROW_NUMBER() OVER (
        PARTITION BY
          dept
-- Ordering DESC inside the window is what makes rn = 1 mean "highest earner"
-- -- flipping to ASC would instead make rn = 1 the LOWEST earner per department.
        ORDER BY
          salary DESC
      ) AS rn
    FROM
-- No WHERE clause at all inside the CTE -- ranked deliberately keeps EVERY row,
-- numbered; filtering down to the top N is entirely the OUTER query's job.
      employee
  )
-- rn itself is intentionally NOT selected in the final output -- it did its job
-- inside the WHERE clause below and has no further meaning to the reader.
SELECT
  name,
  dept,
  salary
FROM
  ranked
-- This WHERE clause is what a naive "WHERE ROW_NUMBER() OVER (...) <= 2" wishes
-- it could be -- Postgres rejects that form outright because window functions
-- are computed AFTER the WHERE clause has already filtered rows, not before.
WHERE
  rn <= 2 -- => keeps only the top 2 earners PER department
-- Ordering by dept groups the two departments' top earners together for
-- display, and salary DESC surfaces each department's #1 first.
ORDER BY
  dept,
  salary DESC;

-- => Engineering: Linus, Ada (Barbara excluded -- 3rd place)
-- => Data: Grace, Alan (Edsger excluded -- 3rd place)
-- Changing "rn <= 2" to any other N (say, 1 for department heads, or 5 for a
-- wider leaderboard) is the ENTIRE change needed to adjust N -- nothing about
-- the ranked CTE itself needs to change.
-- Top-N-per-group via ROW_NUMBER is the general-purpose tool -- DISTINCT ON
-- (a Postgres-specific extension) can express the N=1 special case even more
-- tersely, at the cost of being non-standard SQL.
