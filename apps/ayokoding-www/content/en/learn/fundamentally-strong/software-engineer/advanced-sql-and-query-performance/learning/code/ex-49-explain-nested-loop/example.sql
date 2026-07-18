-- Example 49: EXPLAIN Nested Loop.
-- A Nested Loop join (co-24) is the simplest strategy: for EACH row of the outer
-- side, probe the inner side directly -- cheap when the inner probe is an indexed
-- lookup, and cheaper still when PostgreSQL can CACHE repeated inner lookups (Memoize).
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book, author CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- Deliberately skewed cardinality: 5 authors, 50,000 books -- the LOW-cardinality
-- side (author) is exactly what makes Memoize's caching so effective below.
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL REFERENCES author(id));
INSERT INTO author(id, name) SELECT n, 'Author ' || n FROM generate_series(1, 5) AS n;
                                    -- => only 5 authors -- FEW distinct values on the join key
INSERT INTO book(id, title, author_id)
SELECT n, 'Book ' || n, 1 + (n % 5) FROM generate_series(1, 50000) AS n;
                                    -- => 50,000 books -- every book's author_id is one of only 5 values
CREATE INDEX idx_book_author_id ON book(author_id);
ANALYZE author;
ANALYZE book;

-- Force Nested Loop specifically so the plan is deterministic for this example --
-- production code should NEVER disable other join strategies; this is teaching-only.
-- Disabling the other two strategies is a blunt teaching tool -- it forces
-- the planner's hand so this example's EXPLAIN output is reproducible,
-- regardless of what statistics/cost constants your own Postgres has.
SET enable_hashjoin = off;
SET enable_mergejoin = off;

EXPLAIN SELECT a.name, COUNT(*) AS book_count
FROM author a
JOIN book b ON b.author_id = a.id
GROUP BY a.name;
                                    -- => Nested Loop: book (50,000 rows) is the OUTER side (Seq Scan)
                                    -- => author is the INNER side, probed via Index Scan on author_pkey
                                    -- => Memoize wraps the inner probe -- caches each author_id's lookup,
                                    -- => so only 5 UNIQUE index probes actually happen, not 50,000
