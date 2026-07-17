-- Example 13: UNION vs UNION ALL.
-- UNION (co-07) combines two result sets AND removes duplicate rows -- UNION ALL
-- combines them and KEEPS every duplicate. Same two inputs, different row counts out.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS newsletter_signup,
loyalty_signup CASCADE;

-- => resets state -- this example is fully self-contained
-- Both tables use email as a bare TEXT PRIMARY KEY -- no surrogate id column at
-- all -- deliberately minimal so UNION's row-level comparison has exactly one
-- column to reason about.
CREATE TABLE newsletter_signup (email TEXT PRIMARY KEY);

-- Two structurally IDENTICAL single-column tables (same type, same constraint)
-- -- UNION/UNION ALL require the two SELECTs to return the same NUMBER of
-- columns with compatible types, though the source tables need not match otherwise.
CREATE TABLE loyalty_signup (email TEXT PRIMARY KEY);

-- => two independent lists -- some emails overlap
-- grace@example.com is deliberately seeded into BOTH tables -- the one row
-- UNION will collapse and UNION ALL will duplicate, making the contrast visible.
-- Two rows per table is the minimum needed to demonstrate all three cases at
-- once: an email unique to newsletter, one unique to loyalty, and one shared.
INSERT INTO
  newsletter_signup (email)
VALUES
  ('ada@example.com'),
  ('grace@example.com');

INSERT INTO
  loyalty_signup (email)
VALUES
  ('grace@example.com'),
  ('alan@example.com');

-- => grace@example.com appears in BOTH lists
-- UNION (co-07) de-duplicates: grace@example.com collapses to ONE row in the output.
-- Because email is PRIMARY KEY in each source table, duplicates can only arise
-- ACROSS the two tables (like grace here), never WITHIN a single one -- UNION's
-- de-duplication step is doing real work only on that cross-table overlap.
SELECT
  email
FROM
-- UNION's de-duplication compares ENTIRE output rows for equality -- with a
-- single email column that means exact string equality; a multi-column UNION
-- would require every column to match before two rows count as duplicates.
  newsletter_signup
UNION
SELECT
  email
FROM
  loyalty_signup
-- ORDER BY applies to the COMBINED result of both SELECTs, not to either side
-- individually -- it must reference an output column name/position, not a
-- table-qualified column, since the two source tables no longer exist by this point.
ORDER BY
  email;

-- => 3 rows: ada, alan, grace -- grace appears only ONCE
-- UNION ALL keeps every row from both sides, duplicates included -- grace appears TWICE.
-- UNION ALL is cheaper than UNION whenever duplicates are acceptable (or known
-- impossible) -- it skips the sort/hash step UNION needs internally to detect
-- and remove duplicate rows, which matters once the combined row count is large.
SELECT
  email
FROM
  newsletter_signup
-- Same two source SELECTs as above, same ORDER BY -- UNION ALL is the ONLY
-- thing that changed, isolating exactly what de-duplication costs/changes.
UNION ALL
SELECT
  email
FROM
  loyalty_signup
ORDER BY
  email;

-- => 4 rows: ada, alan, grace, grace -- no de-duplication happened
-- Choosing UNION vs UNION ALL is a correctness decision, not just a performance
-- one -- reaching for UNION ALL on data with real overlap (like these two lists)
-- would silently double-count grace@example.com in any downstream aggregation.
-- Both queries return the SAME 4 total rows from the underlying tables -- only
-- how those rows get COMBINED differs between the two set operators.
