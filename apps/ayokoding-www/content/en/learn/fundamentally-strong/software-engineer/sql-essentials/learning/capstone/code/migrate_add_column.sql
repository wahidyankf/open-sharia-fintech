-- Capstone: migrate_add_column.sql -- an additive migration, Example 59's exact pattern (co-22),
-- applied AFTER schema.sql + seed.sql have already populated book with 3 rows.
ALTER TABLE book ADD COLUMN edition INTEGER DEFAULT 1;
                                    -- => no table rewrite, no downtime -- existing rows read DEFAULT

.headers on
.mode column
SELECT id, title, price, edition FROM book;
                                    -- => all 3 pre-existing rows show edition = 1 -- none broke
