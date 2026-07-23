-- Example 33: RANGE vs ROWS Frame.
-- With a UNIQUE ORDER BY key, RANGE and ROWS frames agree. With DUPLICATE ORDER BY
-- values, they diverge (co-05): RANGE treats every tied "peer" row as ARRIVING
-- together, ROWS treats each physical row as its own step regardless of ties.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS sale CASCADE;

-- => resets state -- this example is fully self-contained
-- A minimal 4-row table with exactly one deliberate tie -- the smallest
-- dataset that can expose a RANGE-vs-ROWS divergence at all.
CREATE TABLE sale (
-- id is never referenced inside either OVER() clause -- only amount drives
-- the ordering and frame boundaries for both window functions here.
  id INTEGER PRIMARY KEY,
  amount NUMERIC(8, 2) NOT NULL
);

-- id doubles as an arbitrary insertion-order tie-breaker -- amount alone
-- cannot distinguish row 2 from row 3, both windows key off amount only.
INSERT INTO
  sale (id, amount)
VALUES
  (1, 10.00),
  (2, 20.00),
  (3, 20.00), -- => TIES with row 2 -- both have amount = 20.00
  (4, 30.00);

-- => rows 2 and 3 are "peers" under ORDER BY amount -- the tie
-- Without a tie, this whole example would have nothing to show -- RANGE and
-- ROWS only disagree when two or more rows share the SAME ORDER BY value.
-- ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW (co-05) walks PHYSICAL rows one
-- at a time -- row 2 and row 3 get DIFFERENT running sums even though they tie.
-- RANGE (the default frame mode) treats BOTH peers as arriving simultaneously --
-- row 2 and row 3 get the SAME running sum, computed as of the whole peer group.
SELECT
  id,
  amount,
-- UNBOUNDED PRECEDING AND CURRENT ROW means "every row from the very start
-- through this one" -- the running-total shape, just with the frame MODE made
-- explicit instead of relying on the default.
  SUM(amount) OVER (
    ORDER BY
      amount ROWS BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) AS rows_frame,
-- This is IDENTICAL to Example 8's default (no explicit frame) behavior --
-- RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW is exactly what Postgres
-- assumes when ORDER BY is present but no frame clause is written at all.
  SUM(amount) OVER (
    ORDER BY
      amount RANGE BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) AS range_frame
FROM
-- Both window functions read from the SAME sale table in the SAME query --
-- only the frame MODE (ROWS vs RANGE) differs between the two OVER() clauses.
  sale
-- Ordering by amount THEN id breaks the tie deterministically for DISPLAY --
-- rows_frame and range_frame's values were already fixed by each window's own
-- ORDER BY amount, independent of this outer tie-break.
ORDER BY
  amount,
  id;

-- => id 2: rows_frame 30.00 (10+20), range_frame 50.00 (10+20+20, BOTH peers)
-- => id 3: rows_frame 50.00 (10+20+20), range_frame 50.00 (SAME as id 2 -- peers tie)
-- The practical rule of thumb: reach for ROWS whenever the frame should be
-- about PHYSICAL row position (exactly N rows), and rely on the RANGE default
-- only when ties in the ORDER BY column should logically move together.
