-- Example 22: Autoincrement Rowid.
-- INTEGER PRIMARY KEY aliases rowid (co-02) -- omitting it lets SQLite pick the next value.
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => author table exists, currently empty

INSERT INTO author(name) VALUES('Ada');
                                    -- => no id supplied -- engine auto-assigns id = 1
INSERT INTO author(name) VALUES('Grace');
                                    -- => engine auto-assigns id = 2 (one higher than the max so far)

.headers on
.mode column
SELECT * FROM author;              -- => ids came from the engine, not from us: 1, then 2
