-- Example 58: Case Expression
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => a single flat table
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  price REAL                                  -- => drives the CASE branch below
);

-- Prices straddle the 20.00 threshold on both sides, plus exactly ON it (book 5).
INSERT INTO book (id, title, price) VALUES     -- => 5 rows spanning the 20.00 threshold
  (1, 'Notes on the Analytical Engine', 25.00), -- => above 20 -- lands in 'premium'
  (2, 'Introduction to Computing', 18.50),      -- => below 20 -- lands in 'standard'
  (3, 'On Computable Numbers', 30.00),          -- => above 20 -- lands in 'premium'
  (4, 'The Enigma Papers', 15.00),              -- => below 20 -- lands in 'standard'
  (5, 'Compilers and Common Sense', 20.00);    -- => exactly 20.00 -- NOT > 20, so 'standard'

-- CASE WHEN ... THEN ... ELSE ... END is an inline conditional expression --
-- it derives a brand-new column value per row, without a separate UPDATE or
-- a client-side loop. WHEN conditions are checked top to bottom, first match wins.
SELECT title, price,                            -- => the raw columns, plus a derived one below
  CASE                                           -- => the derived tier column starts here
    WHEN price > 20 THEN 'premium'              -- => strictly greater than 20
    ELSE 'standard'                              -- => everything else, including = 20
  END AS tier
FROM book                                       -- => the 5-row source table above
ORDER BY id;                                    -- => deterministic row order
