-- Example 61: Migration Version Tracking -- initial schema (version 0, the SQLite default).
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
                                    -- => a fresh database file -- PRAGMA user_version starts at 0
INSERT INTO book(id, title, price) VALUES
    (1, 'Notes on the Analytical Engine', 12.5),
    (2, 'Sketch of the Analytical Engine', 9.0);
                                    -- => 2 pre-existing rows -- the migration below must not break them
