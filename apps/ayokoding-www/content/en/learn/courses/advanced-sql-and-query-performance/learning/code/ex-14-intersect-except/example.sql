-- Example 14: INTERSECT and EXCEPT.
-- INTERSECT (co-07) keeps only rows present in BOTH result sets. EXCEPT keeps rows
-- from the FIRST set that are absent from the second -- order of operands matters.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS newsletter_signup,
loyalty_signup CASCADE;

-- => resets state -- this example is fully self-contained
-- Reuses the exact same two-table, two-row-each shape as Example 13 -- only the
-- SET OPERATOR changes, isolating INTERSECT/EXCEPT semantics from schema noise.
CREATE TABLE newsletter_signup (email TEXT PRIMARY KEY);

-- email TEXT PRIMARY KEY on both tables guarantees no WITHIN-table duplicates
-- exist -- so any de-duplication INTERSECT/EXCEPT perform is purely a function
-- of cross-table overlap, identical in spirit to Example 13's UNION case.
CREATE TABLE loyalty_signup (email TEXT PRIMARY KEY);

-- => two independent lists -- some emails overlap
-- The same overlap pattern as Example 13: grace@example.com seeded into both
-- lists is what makes INTERSECT return exactly one row below.
INSERT INTO
  newsletter_signup (email)
VALUES
  ('ada@example.com'),
  ('grace@example.com');

-- alan@example.com appears ONLY in loyalty_signup -- the mirror-image edge case
-- to ada@example.com, which appears ONLY in newsletter_signup.
INSERT INTO
  loyalty_signup (email)
VALUES
  ('grace@example.com'),
  ('alan@example.com');

-- => grace@example.com is the only email in BOTH lists
-- INTERSECT (co-07) keeps rows appearing on BOTH sides -- only grace qualifies.
-- INTERSECT (unlike INNER JOIN on email) needs no explicit join condition --
-- it compares entire output ROWS between the two SELECTs and keeps only the
-- ones present on BOTH sides, which is a set operation, not a row-matching one.
-- Neither query needs DISTINCT -- INTERSECT and EXCEPT are inherently
-- set-based and de-duplicate their OWN result by default, same as UNION.
SELECT
  email
FROM
  newsletter_signup
-- Both SELECTs must again return the same number/type of columns, exactly as
-- UNION required in Example 13 -- every set operator shares that column-shape rule.
INTERSECT
SELECT
  email
FROM
  loyalty_signup;

-- => 1 row: grace@example.com -- subscribed to BOTH programs
-- EXCEPT keeps rows from the LEFT side with no match on the right -- newsletter
-- subscribers who never joined the loyalty program.
-- EXCEPT is ORDER-SENSITIVE: "newsletter_signup EXCEPT loyalty_signup" reads
-- "newsletter rows with no loyalty match" -- swapping the two SELECTs around
-- EXCEPT would instead surface loyalty-only subscribers (alan@example.com).
SELECT
  email
FROM
  newsletter_signup
-- Some other database systems spell this operator MINUS instead of EXCEPT --
-- Postgres (following the SQL standard) uses EXCEPT; MINUS is not recognized.
EXCEPT
SELECT
  email
FROM
  loyalty_signup;

-- => 1 row: ada@example.com -- newsletter-only, never loyalty
-- INTERSECT and EXCEPT compose the same way UNION does -- they can be chained,
-- wrapped in a CTE, or combined with ORDER BY/LIMIT on the final combined result,
-- though neither query here needed an explicit ORDER BY to get one row back.
