-- Example 10: Row Number vs Rank vs Dense Rank.
-- Three ranking functions (co-06) handle ties differently -- Barbara and Ada below
-- tie on salary, and each function assigns that tie a different rank.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS employee CASCADE;

-- => resets state -- this example is fully self-contained
-- salary alone (no dept) keeps this example focused purely on the three ranking
-- functions' tie-breaking behavior, without PARTITION BY complicating the frame.
CREATE TABLE employee (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
-- salary is NOT NULL -- all three ranking functions treat NULL as sorting last
-- by default (NULLS LAST for DESC), which would need extra handling if it occurred.
  salary NUMERIC(9, 2) NOT NULL
);

-- => employee table exists, currently empty
-- Salaries are chosen so exactly one tie exists (Ada/Barbara at 95000), bracketed
-- by a unique top earner (Linus) and a unique bottom earner (Grace) -- a minimal
-- dataset that still exercises every rank-numbering edge case.
INSERT INTO
  employee (id, name, salary)
VALUES
  (1, 'Linus', 105000),
  (2, 'Ada', 95000),
  (3, 'Barbara', 95000),
  (4, 'Grace', 88000);

-- => Ada and Barbara TIE at 95000 -- the interesting case below
-- ROW_NUMBER gives every row a unique, arbitrary-among-ties number. RANK leaves a
-- GAP after a tie (2, 2, 4). DENSE_RANK leaves NO gap after a tie (2, 2, 3) (co-06).
-- All three functions here share the identical OVER (ORDER BY salary DESC) --
-- the ranking algorithm is the ONLY thing that differs between them, which is
-- exactly what this example isolates by computing all three side by side.
SELECT
  name,
  salary,
-- ROW_NUMBER's tie-break between Ada and Barbara (both 95000) is UNSPECIFIED --
-- without a secondary ORDER BY key, Postgres may return either order, and that
-- order can even change between runs on a larger, un-vacuumed table.
  ROW_NUMBER() OVER (
    ORDER BY
      salary DESC
  ) AS row_num,
-- RANK() literally counts how many rows sort ahead of (or tied with) the current
-- one, then adds 1 -- two rows tied for 2nd push the next distinct value to rnk 4,
-- because two rows already occupy ranks 2 and 3 in the underlying count.
  RANK() OVER (
    ORDER BY
      salary DESC
  ) AS rnk,
-- DENSE_RANK() instead counts DISTINCT preceding values -- a tie still shares
-- rank 2, but the next distinct salary becomes rank 3, not 4, because ties never
-- consume extra rank "slots". Choose RANK for leaderboard-style gaps, DENSE_RANK
-- for compact tier numbering (e.g. "top 3 distinct price tiers").
  DENSE_RANK() OVER (
    ORDER BY
      salary DESC
  ) AS dense_rnk
FROM
  employee
-- "salary DESC, name" gives the display a deterministic tie-break (alphabetical
-- by name) -- this ordering is cosmetic only; it does not change the row_num/rnk/
-- dense_rnk VALUES already computed by the window ORDER BY inside each OVER().
ORDER BY
  salary DESC,
  name;

-- => Ada/Barbara tie: row_num 2 vs 3 (arbitrary among ties)
-- => Ada/Barbara tie: rnk 2 and 2 -- Grace then jumps to rnk 4
-- => Ada/Barbara tie: dense_rnk 2 and 2 -- Grace is dense_rnk 3
-- The three columns together are the whole point: identical input, identical
-- ORDER BY, three genuinely different numbering strategies for the exact same tie.
