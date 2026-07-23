-- Example 16: Select Distinct.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, author_id) VALUES
    (1, 'The Pragmatic Programmer', 1),  -- => author_id 1 -- first occurrence
    (2, 'Clean Code', 1),                -- => author_id 1 -- a duplicate value
    (3, 'The Mythical Man-Month', 2);      -- => author_id 2 -- first occurrence

-- turn on headers + column alignment so the result below reads as a table
.headers on
.mode column
-- DISTINCT (co-08) collapses duplicate result rows -- here, two books share author_id 1.
SELECT DISTINCT author_id FROM book;
                                    -- => 3 input rows collapse to 2 distinct author_id values
