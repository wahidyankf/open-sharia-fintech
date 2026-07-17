-- Kata 10 (before): a materialized view is a SNAPSHOT -- writing to the base
-- table never touches it, and no error warns a reader the numbers are stale.
SET client_min_messages TO WARNING;
DROP MATERIALIZED VIEW IF EXISTS author_revenue CASCADE;
DROP TABLE IF EXISTS book CASCADE;
CREATE TABLE book(id INTEGER PRIMARY KEY, author_id INTEGER NOT NULL, price NUMERIC(8,2) NOT NULL);
INSERT INTO book(id, author_id, price) VALUES (1, 1, 40.00), (2, 1, 20.00);
CREATE MATERIALIZED VIEW author_revenue AS
    SELECT author_id, SUM(price) AS total FROM book GROUP BY author_id;
-- author 1's total is captured HERE, at CREATE time: 60.00

-- a new book is added to the SAME author AFTER the view was built.
INSERT INTO book(id, author_id, price) VALUES (3, 1, 100.00);

-- BUG: reading the materialized view still returns the OLD total -- no
-- REFRESH was ever issued, and PostgreSQL never auto-refreshes it for you.
SELECT author_id, total FROM author_revenue;
