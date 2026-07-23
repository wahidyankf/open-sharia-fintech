-- Example 12: NTILE Quartiles.
-- NTILE(4) (co-06) splits the ordered row set into 4 AS-EQUAL-AS-POSSIBLE buckets
-- and labels each row with its bucket number -- 1 (top) through 4 (bottom) here.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS employee CASCADE;

-- => resets state -- this example is fully self-contained
CREATE TABLE employee (
-- id values are not used anywhere in the SELECT -- name alone is enough to
-- identify each row in the output, but a primary key still documents uniqueness.
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
-- Eight distinct salary values, no ties -- keeps this example focused on NTILE's
-- bucketing mechanics rather than on how it handles tied input values.
  salary NUMERIC(9, 2) NOT NULL
);

-- => employee table exists, currently empty
-- 8 employees is a deliberately EVEN multiple of 4 -- NTILE splits cleanly into
-- equal buckets only when row_count is divisible by the bucket count; otherwise
-- the earlier buckets silently absorb the extra rows (see the note below).
INSERT INTO
  employee (id, name, salary)
VALUES
  (1, 'Linus', 120000),
  (2, 'Grace', 110000),
  (3, 'Ada', 100000),
  (4, 'Alan', 95000),
  (5, 'Barbara', 90000),
  (6, 'Edsger', 85000),
  (7, 'Donald', 80000),
  (8, 'Margaret', 75000);

-- => 8 employees -- NTILE(4) puts exactly 2 rows per bucket
-- NTILE(4) OVER (ORDER BY salary DESC) (co-06) assigns bucket 1 to the top 2
-- earners, bucket 2 to the next 2, and so on down to bucket 4.
-- NTILE takes the DESIRED bucket count as its argument, not a row-count-per-
-- bucket -- Postgres works out row distribution FROM that count, which is why
-- exactly 2 employees land in each of the 4 buckets here (8 rows / 4 buckets).
SELECT
  name,
  salary,
-- Ordering DESC means bucket 1 gets the HIGHEST salaries -- flipping to ASC
-- would relabel the same employees, but bucket 1 would then be the LOWEST
-- earners instead; NTILE itself has no notion of "top" or "bottom".
  NTILE (4) OVER (
    ORDER BY
      salary DESC
  ) AS salary_quartile
FROM
-- If row_count were NOT evenly divisible by 4 (say, 9 employees), Postgres
-- distributes the remainder to the EARLIEST buckets in ORDER BY sequence --
-- bucket 1 would get 3 rows and buckets 2-4 would get 2 rows each, for example.
  employee
-- The outer ORDER BY salary DESC matches the window's internal ordering here,
-- purely so the printed rows read top-to-bottom by quartile -- NTILE's bucket
-- assignment was already fixed by the window's own ORDER BY, independent of this.
ORDER BY
  salary DESC;

-- => Linus, Grace: quartile 1 (top earners)
-- => Donald, Margaret: quartile 4 (bottom earners)
-- Unlike RANK/DENSE_RANK, NTILE ignores VALUE ties entirely -- two employees
-- with identical salaries straddling a bucket boundary would still be split
-- into different quartiles, based purely on row position, not on the tied value.
