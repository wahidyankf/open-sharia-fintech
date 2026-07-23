-- Kata 4 (after): ROW_NUMBER() with a deterministic tiebreaker caps at exactly N.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book CASCADE;
CREATE TABLE book(id INTEGER PRIMARY KEY, author_id INTEGER NOT NULL, title TEXT NOT NULL, price NUMERIC(6,2) NOT NULL);
INSERT INTO book(id, author_id, title, price) VALUES
    (1, 1, 'Refactoring',            45.00),
    (2, 1, 'Domain-Driven Design',   40.00),
    (3, 1, 'Clean Code',             40.00),
    (4, 1, 'Working Effectively',    30.00);

-- THE FIX: ROW_NUMBER() assigns a UNIQUE, strictly increasing number per row --
-- id is added as a tiebreaker so the choice among tied prices is reproducible.
SELECT author_id, title, price, rn
FROM (
    SELECT author_id, title, price,
           ROW_NUMBER() OVER (PARTITION BY author_id ORDER BY price DESC, id) AS rn
    FROM book
) ranked
WHERE rn <= 2
ORDER BY author_id, price DESC, title;
