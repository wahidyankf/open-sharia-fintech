-- Example 20: Default Value.
-- DEFAULT (co-04) supplies a value automatically when an INSERT omits that column.
CREATE TABLE account(id INTEGER PRIMARY KEY, status TEXT DEFAULT 'active');

-- This INSERT lists only id -- status is left out entirely, not set to NULL.
INSERT INTO account(id) VALUES(1);
                                    -- => the engine substitutes 'active' for the missing column

.headers on
.mode column
SELECT * FROM account;             -- => status shows 'active' even though we never wrote it
