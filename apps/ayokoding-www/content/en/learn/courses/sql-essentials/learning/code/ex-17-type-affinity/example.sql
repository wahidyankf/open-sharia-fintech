-- Example 17: Type Affinity.
-- SQLite uses type AFFINITY (co-06), not rigid enforcement -- a declared type is a
-- storage-class preference the engine tries to honor, not a hard runtime barrier.
CREATE TABLE demo(n INTEGER);

-- '42' is a TEXT literal, but the column's INTEGER affinity converts it on insert.
INSERT INTO demo(n) VALUES('42');   -- => the string '42' gets stored as the integer 42

.headers on
.mode column
-- typeof() reveals the ACTUAL storage class the engine chose, not the declared type.
SELECT n, typeof(n) FROM demo;     -- => typeof(n) reports "integer" -- affinity coerced it
