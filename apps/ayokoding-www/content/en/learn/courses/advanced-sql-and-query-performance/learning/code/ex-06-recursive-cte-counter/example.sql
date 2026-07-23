-- Example 6: Recursive CTE Counter.
-- WITH RECURSIVE (co-03) has two parts UNION ALL'd together: a non-recursive
-- "anchor" (the starting row) and a "recursive" term that refers back to the CTE's
-- own name -- the engine repeats the recursive term until it returns zero rows.
-- Suppress routine NOTICE messages (e.g. table-does-not-exist-yet on a
-- fresh database) so output below stays focused on the query results.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;

-- => no domain tables needed -- this example is pure logic
-- counter(n) starts at 1 (the anchor). The recursive term adds 1 each pass and
-- WHERE n < 10 is the termination guard -- without it, this would loop forever.
-- UNION ALL (not UNION) is required here for both correctness and speed: plain
-- UNION would deduplicate rows every pass, which is wasted work for values that
-- are already known distinct, and would silently break recursion patterns where
-- legitimate duplicate rows are expected.
WITH RECURSIVE
-- The column list "counter (n)" names the CTE's single output column up front --
-- an alternative would be to alias it per-branch (SELECT 1 AS n), but naming it
-- once on the CTE avoids having to repeat/match the alias in every UNION branch.
  counter (n) AS (
    SELECT
      1 -- => anchor: the FIRST row, n = 1
    UNION ALL
    SELECT
      n + 1
-- Referencing counter here is only legal because this SELECT is the recursive
-- term of a WITH RECURSIVE clause -- a self-reference like this anywhere else
-- would raise "relation counter does not exist". Standard recursive CTEs also
-- allow the self-reference to appear only ONCE per recursive term.
    FROM
      counter
    WHERE
-- Unlike some other database engines, Postgres has no built-in recursion depth
-- limit -- an unbounded recursive CTE (e.g. accidentally using n <= n, always
-- true) will consume memory until it errors or exhausts the server; the WHERE
-- guard here is the only thing standing between this query and that failure mode.
      n < 10
      -- => recursive term: re-reads counter's own
      -- => output from the PREVIOUS pass, adds 1
  )
SELECT
  n
FROM
  counter;

-- => 10 rows: 1, 2, 3, ..., 10 -- the guard stopped it there
