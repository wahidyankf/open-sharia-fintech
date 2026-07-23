-- Example 2: Correlated Subquery.
-- A correlated subquery (co-01) references a column from the OUTER query -- here,
-- a.id -- so the engine conceptually re-evaluates it once per outer row.
-- Suppress routine NOTICE messages (e.g. table-does-not-exist-yet on a
-- fresh database) so output below stays focused on the query results.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;

-- => resets state -- this example is fully self-contained
CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => author table exists, currently empty
CREATE TABLE book (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  price NUMERIC(6, 2) NOT NULL,
  author_id INTEGER REFERENCES author (id)
);

-- => book table exists, currently empty
-- Turing is seeded specifically to exercise the zero-books edge case -- EXISTS
-- must correctly return FALSE (not NULL, not an error) when the correlated
-- inner query finds no matching rows at all for that outer row.
INSERT INTO
  author (id, name)
VALUES
  (1, 'Ada Lovelace'),
  (2, 'Grace Hopper'),
  (3, 'Alan Turing');

-- => 3 authors -- Turing has no books at all (seeded below)
-- Hopper's single book is priced BELOW the $30 filter -- this exercises the case
-- where EXISTS finds a correlated row but the AND condition inside still fails,
-- which is different from finding zero rows at all (Turing's case above).
INSERT INTO
  book (id, title, price, author_id)
VALUES
  (1, 'The Pragmatic Programmer', 34.99, 1),
  (2, 'Clean Code', 29.99, 1),
  (3, 'The Mythical Man-Month', 24.50, 2);

-- => Ada has 2 books above $30 threshold used below
-- EXISTS(...) (co-01) is TRUE the moment the inner query finds ONE matching row --
-- b.author_id = a.id makes this correlated: the inner query changes per outer row.
-- Conceptually the inner query re-runs once per outer author row, substituting
-- a.id afresh each time -- but the Postgres planner does not literally loop;
-- it typically rewrites EXISTS(...) into a semi-join and can use an index on
-- book.author_id to avoid a full re-scan per outer row (see EXPLAIN examples later).
-- Table aliases (author a, book b) are required here because the correlation
-- predicate b.author_id = a.id must unambiguously reference both the outer
-- and inner table -- Postgres cannot infer which "id" column without them.
-- EXISTS produces a boolean, so it composes naturally as a WHERE-clause predicate
-- on its own -- no comparison operator or NULL-handling wrapper is needed.
SELECT
  a.name
FROM
  author a
WHERE
  EXISTS (
-- SELECT 1 (not SELECT * or a real column) is idiomatic inside EXISTS -- the
-- planner only cares whether a row EXISTS, never the projected values, so
-- selecting a constant avoids any wasted column materialization.
    SELECT
      1
    FROM
      book b
    WHERE
-- The AND condition is evaluated INSIDE the correlated scope, alongside the
-- correlation predicate itself -- both must hold on the SAME inner row for
-- EXISTS to return TRUE for this particular outer author.
      b.author_id = a.id
      AND b.price > 30
  );

-- => Ada: has a book priced 34.99 > 30 -- EXISTS is true
-- => Hopper: her only book is 24.50 -- EXISTS is false
-- => Turing: zero books -- EXISTS is false, no rows to check
-- Unlike the equivalent NOT IN pattern, EXISTS/NOT EXISTS never trips on NULL
-- author_id values in the inner query -- this predictable three-value-logic
-- behavior is why EXISTS is generally the safer correlated-subquery idiom.
