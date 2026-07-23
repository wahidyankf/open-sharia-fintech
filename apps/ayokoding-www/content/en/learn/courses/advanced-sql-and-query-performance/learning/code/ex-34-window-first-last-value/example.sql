-- Example 34: FIRST_VALUE and LAST_VALUE.
-- FIRST_VALUE/LAST_VALUE (co-04) read a value from the EDGE of the current frame.
-- The classic gotcha: LAST_VALUE with the DEFAULT frame (RANGE ... UNBOUNDED
-- PRECEDING AND CURRENT ROW, co-05) sees the CURRENT row as the last row -- not
-- the true last row of the partition -- unless the frame is widened explicitly.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS employee CASCADE;

-- => resets state -- this example is fully self-contained
-- Single-department dataset (all Engineering) keeps PARTITION BY trivial here --
-- the interesting behavior is entirely about frame boundaries within one partition.
CREATE TABLE employee (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
-- dept is constant (Engineering) across all 3 rows here -- PARTITION BY still
-- works correctly with a single partition, it just has nothing to contrast
-- against in this minimal example.
  dept TEXT NOT NULL,
-- Same money-safe NUMERIC precision convention used throughout this topic's
-- salary/price columns.
  salary NUMERIC(9, 2) NOT NULL
);

-- Salaries strictly decrease by insertion order -- irrelevant to the query,
-- which orders by salary DESC regardless of insertion order.
INSERT INTO
  employee (id, name, dept, salary)
VALUES
  (1, 'Linus', 'Engineering', 105000),
  (2, 'Ada', 'Engineering', 95000),
  (3, 'Barbara', 'Engineering', 88000);

-- => 3 Engineering employees, ordered by salary DESC below
-- FIRST_VALUE (co-04) with the default frame correctly returns Linus (highest
-- salary) for every row -- the frame's start is fixed at the partition's start.
-- last_value_wrong uses the DEFAULT frame, so it wrongly echoes each row's OWN
-- salary owner back. last_value_fixed widens the frame to the WHOLE partition.
SELECT
  name,
  salary,
-- FIRST_VALUE's default frame -- RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT
-- ROW -- always includes the partition's FIRST row (Linus, once ordered DESC),
-- so FIRST_VALUE is correct with no extra frame clause needed.
  FIRST_VALUE (name) OVER (
-- PARTITION BY dept means each department would get its OWN highest_paid/
-- last_value if more than one department existed -- moot here with just one.
    PARTITION BY
      dept
    ORDER BY
      salary DESC
  ) AS highest_paid,
-- LAST_VALUE's default frame ALSO ends at CURRENT ROW, not at the partition's
-- true last row -- so LAST_VALUE, unlike FIRST_VALUE, silently returns the
-- CURRENT row's own name for every row: the classic default-frame gotcha.
  LAST_VALUE (name) OVER (
    PARTITION BY
      dept
    ORDER BY
      salary DESC
  ) AS last_value_wrong,
-- ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING widens the frame to
-- the ENTIRE partition, front to back -- only then does LAST_VALUE actually
-- reach the partition's true last row (Barbara) for every output row.
  LAST_VALUE (name) OVER (
    PARTITION BY
      dept
    ORDER BY
      salary DESC ROWS BETWEEN UNBOUNDED PRECEDING
      AND UNBOUNDED FOLLOWING
  ) AS last_value_fixed
FROM
-- All three window functions read the SAME partition/order specification,
-- differing only in their FRAME -- isolating frame width as the one variable.
  employee
-- Ordering DESC for display matches the DESC ordering already used inside
-- every OVER() clause -- Linus (highest) prints first, Barbara (lowest) last.
ORDER BY
  salary DESC;

-- => highest_paid is Linus for ALL 3 rows -- correct on the first try
-- => last_value_wrong just echoes each row's OWN name -- the gotcha
-- => last_value_fixed is Barbara for ALL 3 rows -- the TRUE lowest earner
-- MIN()/MAX() OVER (PARTITION BY dept) would sidestep this whole gotcha for a
-- simple highest/lowest lookup -- FIRST_VALUE/LAST_VALUE earn their keep once
-- you need an arbitrary EXPRESSION evaluated at a specific frame edge, not just
-- the min/max of one column.
