-- Example 50: EXPLAIN Hash Join.
-- A Hash Join (co-24) builds an in-memory hash table from the SMALLER side, then
-- probes it once per row of the larger side -- effective when NEITHER side has a
-- usable index for the join condition, unlike Example 49's indexed Nested Loop.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book_catalog, publisher CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- Neither table gets an index on the join column -- a deliberate choice that
-- takes Nested Loop and Merge Join both off the table as competitive options.
CREATE TABLE publisher(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
INSERT INTO publisher(id, name) SELECT n, 'Publisher ' || n FROM generate_series(1, 500) AS n;
                                    -- => 500 publishers -- the "build" side for the hash table
CREATE TABLE book_catalog(id INTEGER PRIMARY KEY, title TEXT NOT NULL, publisher_id INTEGER NOT NULL);
INSERT INTO book_catalog(id, title, publisher_id)
SELECT n, 'Book ' || n, 1 + (n % 500) FROM generate_series(1, 100000) AS n;
                                    -- => 100,000 books -- the "probe" side, NO index on publisher_id
ANALYZE publisher;
ANALYZE book_catalog;
                                    -- => deliberately no index on book_catalog.publisher_id

-- Force Hash Join specifically so the plan is deterministic -- production code
-- should never disable other join strategies; this is teaching-only.
-- With no index on either join column, Postgres would likely pick Hash Join
-- anyway -- these SET statements exist mainly to make the choice deterministic
-- and self-documenting rather than to override a close planner decision.
SET enable_nestloop = off;
SET enable_mergejoin = off;

EXPLAIN SELECT p.name, COUNT(*) AS book_count
FROM publisher p
JOIN book_catalog bc ON bc.publisher_id = p.id
GROUP BY p.name;
                                    -- => Hash Join: publisher (500 rows) builds the in-memory hash table
                                    -- => book_catalog (100,000 rows) is scanned once, probing the hash table
                                    -- => Seq Scan on BOTH sides -- neither side has an index to exploit
