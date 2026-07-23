-- Example 3: Insert Single Row.
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => author table exists, currently empty (0 rows)

-- INSERT INTO ... VALUES (co-10) adds exactly one new row to the relation.
INSERT INTO author(name) VALUES('Ada');
                                    -- => id is omitted -- INTEGER PRIMARY KEY auto-assigns 1
                                    -- => author now holds exactly one row: (1, 'Ada')

-- dot-commands take the rest of their line as arguments -- comments live on their own line.
.headers on
-- => turns on a column-name header row for readability
.mode column
-- => aligns SELECT output into fixed-width columns
SELECT * FROM author;              -- => projects every column of every row -- confirms one row
