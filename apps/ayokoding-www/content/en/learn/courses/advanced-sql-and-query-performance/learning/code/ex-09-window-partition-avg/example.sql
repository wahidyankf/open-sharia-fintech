-- Example 9: Window Partition Avg.
-- PARTITION BY (co-05) splits the window into independent groups -- the AVG below
-- resets per department instead of averaging across the whole company.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS employee CASCADE;

-- => resets state -- this example is fully self-contained
-- dept is stored as plain TEXT here rather than a normalized department table --
-- fine for this example's teaching purpose; a real schema might use a dept_id FK.
CREATE TABLE employee (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
-- dept is NOT NULL -- PARTITION BY treats NULL as its own group if it ever
-- appeared, which would silently create a third "unknown department" partition.
  dept TEXT NOT NULL,
-- NUMERIC(9, 2) accommodates salaries up to 9,999,999.99 -- comfortably above
-- any individual value here, with headroom for a SUM() OVER() variant of this
-- query that would total multiple employees' salaries together.
  salary NUMERIC(9, 2) NOT NULL
);

-- => employee table exists, currently empty
INSERT INTO
  employee (id, name, dept, salary)
VALUES
  (1, 'Ada', 'Engineering', 95000),
  (2, 'Linus', 'Engineering', 105000),
  (3, 'Barbara', 'Engineering', 88000),
  (4, 'Grace', 'Data', 99000),
  (5, 'Alan', 'Data', 91000);

-- => 3 Engineering rows, 2 Data rows -- two separate partitions
-- AVG(salary) OVER (PARTITION BY dept) (co-05) computes each department's OWN
-- average, independent of the other department -- every row still appears, unlike
-- GROUP BY which would collapse each dept down to one summary row.
-- This OVER() has PARTITION BY but NO ORDER BY -- with no ordering, the window
-- frame defaults to the ENTIRE partition (every row sharing the same dept),
-- not a running subset. Contrast with Example 8, where adding ORDER BY narrowed
-- the frame down to "from the start through the current row" instead.
SELECT
  name,
  dept,
  salary,
-- ROUND() wraps the window function's result -- this is legal because ROUND is
-- an ordinary scalar function applied AFTER AVG(...) OVER(...) produces its
-- value; nesting one window function directly inside ANOTHER window function's
-- argument, by contrast, is not allowed.
  ROUND(
    AVG(salary) OVER (
      PARTITION BY
        dept
    ),
    2
  ) AS dept_avg_salary
FROM
-- No JOIN or GROUP BY is needed to get a per-department average alongside every
-- individual employee row -- this is precisely the row-preserving property that
-- distinguishes window functions from GROUP BY aggregation.
  employee
-- Ordering by dept groups the two partitions visually together in the output,
-- and salary DESC within each dept surfaces the highest earner first -- neither
-- ordering choice affects the already-computed dept_avg_salary values themselves.
ORDER BY
  dept,
  salary DESC;

-- => Engineering avg (95000+105000+88000)/3 = 96000.00
-- => Data avg (99000+91000)/2 = 95000.00 -- a DIFFERENT partition
-- dept_avg_salary is IDENTICAL for every row within the same department --
-- that repetition (95000.00 appears on both Data rows) is the visible signature
-- of a window function: it decorates each row rather than collapsing them.
