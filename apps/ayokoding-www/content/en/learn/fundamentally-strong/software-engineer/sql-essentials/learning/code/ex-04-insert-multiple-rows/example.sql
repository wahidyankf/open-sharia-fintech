-- Example 4: Insert Multiple Rows.
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => author table exists, ready for a bulk insert

-- One INSERT statement, three comma-separated value tuples (co-10) -- a single
-- round-trip to the engine instead of three separate INSERT statements.
INSERT INTO author(name) VALUES
    ('Ada Lovelace'),               -- => row 1: id auto-assigns to 1
    ('Grace Hopper'),                -- => row 2: id auto-assigns to 2
    ('Alan Turing');                 -- => row 3: id auto-assigns to 3

.headers on
.mode column
-- => the pair above produces an aligned, headered table for readability
SELECT count(*) FROM author;        -- => count(*) counts every row -- confirms all 3 landed
