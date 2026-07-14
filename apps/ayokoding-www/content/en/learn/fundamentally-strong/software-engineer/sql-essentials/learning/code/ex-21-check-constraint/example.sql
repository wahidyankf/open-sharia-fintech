-- Example 21: Check Constraint.
-- CHECK (co-04) enforces an arbitrary boolean expression on every write to that row.
CREATE TABLE book(id INTEGER PRIMARY KEY, price REAL CHECK(price >= 0));

-- -5 violates price >= 0 -- a business invariant the schema itself now guarantees.
INSERT INTO book(price) VALUES(-5);
                                    -- => the engine evaluates CHECK(price >= 0) as false
                                    -- => raises: CHECK constraint failed: price >= 0

.headers on
.mode column
SELECT count(*) FROM book;         -- => confirms the rejected row never landed -- table stays empty
