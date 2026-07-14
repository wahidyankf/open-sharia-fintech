-- Example 61: the migration body itself -- only ever meant to run ONCE, guarded by migrate.sh.
ALTER TABLE book ADD COLUMN edition INTEGER DEFAULT 1;
                                    -- => the additive change, identical in shape to Example 59

-- PRAGMA user_version stores a plain integer INSIDE the database file's header (co-24) --
-- no extra "schema_migrations" table needed to remember which migration already ran.
PRAGMA user_version = 1;
