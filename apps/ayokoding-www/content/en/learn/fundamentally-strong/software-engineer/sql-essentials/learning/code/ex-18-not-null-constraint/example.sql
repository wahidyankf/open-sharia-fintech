-- Example 18: Not Null Constraint.
-- NOT NULL (co-04) is an invariant the engine enforces on EVERY write, not a suggestion.
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- This INSERT explicitly supplies NULL for a column the schema forbids NULL on.
INSERT INTO author(name) VALUES(NULL);
                                    -- => the engine rejects the write before it commits
                                    -- => raises: NOT NULL constraint failed: author.name

.headers on
.mode column
SELECT count(*) FROM author;       -- => confirms the rejected row never landed -- table stays empty
