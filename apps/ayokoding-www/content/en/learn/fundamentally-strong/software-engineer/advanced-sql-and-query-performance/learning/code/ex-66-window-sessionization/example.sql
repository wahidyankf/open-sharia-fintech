-- Example 66: Window Sessionization.
-- A "gaps and islands" session split (co-04, co-05): group consecutive events into
-- a session whenever the gap between them exceeds a threshold -- LAG() measures the
-- gap, then a running SUM() of "new session" flags assigns each row its session id.
-- Suppress routine NOTICE messages so output below stays focused on the query results.
SET
  client_min_messages TO WARNING;

-- CASCADE is a no-op safety net here -- no other table references
-- click_event, but it costs nothing to include for a clean, idempotent reset.
DROP TABLE IF EXISTS click_event CASCADE;

-- => resets state -- this example is fully self-contained
-- clicked_at is TIMESTAMP (not TIMESTAMPTZ) for simplicity -- the gap
-- computation below only cares about the DIFFERENCE between two timestamps,
-- so timezone handling is out of scope for this teaching example.
CREATE TABLE click_event (
  -- id is a simple surrogate key -- it plays no role in the sessionization
  -- logic itself, which relies entirely on user_id and clicked_at.
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  clicked_at TIMESTAMP NOT NULL
);

-- Five clicks from a single user, with gaps deliberately chosen around the 30-
-- minute threshold: two short gaps (5 min) that should MERGE into a session,
-- and two long gaps (40 min, 100 min) that should each START a new one.
INSERT INTO
  click_event (id, user_id, clicked_at)
VALUES
  -- row 1 has no previous row for this user, so LAG() returns NULL here --
  -- that NULL is exactly what starts session 0 below.
  (1, 1, '2026-01-01 09:00:00'),
  (2, 1, '2026-01-01 09:05:00'), -- => 5 min gap -- same session
  (3, 1, '2026-01-01 09:45:00'), -- => 40 min gap -- NEW session (threshold is 30 min)
  (4, 1, '2026-01-01 09:50:00'), -- => 5 min gap -- same session as row 3
  (5, 1, '2026-01-01 11:30:00');

-- => 100 min gap -- NEW session again
-- This query builds its answer in THREE stages (gaps, then flagged, then the
-- final SELECT) -- each CTE layer does exactly ONE conceptual step, making the
-- overall sessionization logic easy to verify stage by stage.
-- Stacking CTEs like this (gaps -> flagged -> final SELECT) is a common
-- pattern for multi-step window-function pipelines -- each stage stays
-- readable, and EXPLAIN can show exactly where time goes per stage.
WITH
  gaps AS (
    -- Stage 1: compute how much time elapsed since each user's PREVIOUS click.
    SELECT
      id,
      user_id,
      clicked_at,
      clicked_at - LAG (clicked_at) OVER (
      -- PARTITION BY user_id (co-04) is what keeps each user's session
      -- numbering independent -- without it, LAG() would compare across
      -- DIFFERENT users' click streams, producing meaningless gaps.
        PARTITION BY
          user_id
        ORDER BY
          clicked_at
      ) AS gap
      -- => LAG() (co-04): the PREVIOUS row's timestamp, per user, in order --
      -- => NULL for each user's very first row (no previous row to compare)
    -- Reads directly from the base table -- this CTE is the ONLY place
    -- click_event is ever scanned in the whole query.
    FROM
      click_event
  ),
  flagged AS (
    -- Stage 2: turn each row's gap into a binary 1-or-0 flag -- 1 means "this
    -- row starts a brand-new session," 0 means "this row continues the
    -- previous session."
    SELECT
      id,
      user_id,
      clicked_at,
      -- The OR here means EITHER condition alone is sufficient to start a new
      -- session -- Postgres evaluates OR short-circuit left to right, so a NULL
      -- gap never even reaches the INTERVAL comparison.
      CASE
        -- Comparing to NULL requires IS NULL, not = NULL -- ordinary equality
        -- against NULL always evaluates to UNKNOWN, never TRUE, in SQL.
        WHEN gap IS NULL
        OR gap > INTERVAL '30 minutes' THEN 1
        ELSE 0
      END AS is_new_session
      -- => a gap of NULL (first row) or > 30 min STARTS a new session
    FROM
      gaps
  )
-- An alternative design would use LEAD() instead of a running SUM(), but that
-- approach only tells you WHERE a boundary is, not which session NUMBER a row
-- belongs to -- the running SUM() trick solves both in a single pass.
-- Stage 3: a running SUM() over the is_new_session flags turns "is this row a
-- session boundary" into "which session number does this row belong to" -- the
-- classic gaps-and-islands trick for turning a boolean signal into a group id.
SELECT
  id,
  user_id,
  clicked_at,
  SUM(is_new_session) OVER (
    PARTITION BY
      user_id
    ORDER BY
    -- An EXPLICIT ROWS frame (co-05) is required here -- the default frame for
    -- a window ORDER BY (RANGE UNBOUNDED PRECEDING) would silently group PEER
    -- rows with identical clicked_at values together, which is not what a
    -- session-numbering running total needs.
      clicked_at ROWS BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) AS session_id
  -- => running SUM() of the flag (co-05, explicit ROWS frame) --
  -- => each "new session" flag PERMANENTLY bumps the session number
  -- => for every subsequent row, exactly like a running total
FROM
  flagged
-- Ordering the FINAL result by user_id then clicked_at makes each user's
-- session progression easy to read top to bottom, though it plays no role
-- in the session_id computation itself (that already happened above).
ORDER BY
  user_id,
  clicked_at;
-- The final result assigns session_id 0 to rows 1-2, session_id 1 to rows 3-4,
-- and session_id 2 to row 5 -- matching the three visually distinct clusters
-- of activity implied by the gaps in the seed data above.
