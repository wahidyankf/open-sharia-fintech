-- Example 19: Unique Constraint.
-- UNIQUE (co-04) forbids two rows from sharing the same value in that column.
CREATE TABLE author(id INTEGER PRIMARY KEY, email TEXT UNIQUE);

INSERT INTO author(email) VALUES('ada@example.com');
                                    -- => first insert succeeds -- no prior row to conflict with

-- Same email value again -- the UNIQUE index the engine built now blocks this write.
INSERT INTO author(email) VALUES('ada@example.com');
                                    -- => the engine rejects the duplicate before it commits
                                    -- => raises: UNIQUE constraint failed: author.email

.headers on
.mode column
SELECT count(*) FROM author;       -- => confirms exactly one row survived -- the duplicate never landed
