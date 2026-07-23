-- Example 75: Export Query to CSV.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
                                    -- => a single table -- enough to demonstrate export
INSERT INTO book(id, title, price) VALUES  -- a 2-row multi-VALUES insert
    (1, 'Notes on the Analytical Engine', 12.5),  -- row 1 -- exported below
    (2, 'Sketch of the Analytical Engine', 9.0);   -- row 2 -- exported below

-- .headers on, .mode csv, and .output out.csv below are display/format preferences only.
.headers on
.mode csv
.output out.csv
-- .output REDIRECTS every subsequent result to the named file -- nothing prints to the terminal
-- until .output stdout runs again (co-24). Note: no trailing "--" comment on a dot-command line.
SELECT id, title, price FROM book; -- => written to out.csv, NOT the terminal, while redirected
.output stdout
-- Back on the terminal -- confirms the CLI itself is unaffected by the redirect that just ended.
SELECT 'export done' AS status;    -- => prints on the terminal -- proves .output stdout worked
