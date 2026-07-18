-- Kata 10 (after): REFRESH MATERIALIZED VIEW re-runs the defining query,
-- replacing the stale snapshot with current data.
SET client_min_messages TO WARNING;
DROP MATERIALIZED VIEW IF EXISTS author_revenue CASCADE;
DROP TABLE IF EXISTS book CASCADE;
CREATE TABLE book(id INTEGER PRIMARY KEY, author_id INTEGER NOT NULL, price NUMERIC(8,2) NOT NULL);
INSERT INTO book(id, author_id, price) VALUES (1, 1, 40.00), (2, 1, 20.00);
CREATE MATERIALIZED VIEW author_revenue AS
    SELECT author_id, SUM(price) AS total FROM book GROUP BY author_id;

INSERT INTO book(id, author_id, price) VALUES (3, 1, 100.00);

-- THE FIX: REFRESH MATERIALIZED VIEW (co-27) re-executes the defining query
-- NOW, replacing every row in the view with a fresh result.
REFRESH MATERIALIZED VIEW author_revenue;

SELECT author_id, total FROM author_revenue;
