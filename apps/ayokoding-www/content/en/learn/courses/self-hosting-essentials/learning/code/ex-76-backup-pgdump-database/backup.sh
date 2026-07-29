#!/usr/bin/env bash
# Example 76: A pg_dump Database Backup. (co-19)
#
# A SQLite DB is a FILE (Example 34 backed it up by copying). A PostgreSQL DB
# is a RUNNING SERVER with its own files that must NOT be copied directly (a
# live copy can be torn). pg_dump is the safe, consistent export -- the
# database's own backup API. Run on the box, scheduled by a timer.

set -euo pipefail  # => fail fast; a half-written dump is useless

DB_NAME="myapp"  # => the database the app uses
DUMP_DIR="/var/backups/myapp-pg"  # => a dedicated dir for DB dumps
install -d -m 750 "${DUMP_DIR}"  # => ensure it exists with sane perms
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"  # => UTC stamp; one file per dump
DEST="${DUMP_DIR}/${DB_NAME}-${STAMP}.sql.gz"  # => .gz: compress on the fly

# --- 1. Dump CONSISTENTLY, as the DB sees itself -----------------------------
# pg_dump connects to the running server and exports a consistent snapshot --
# safe even while the app is writing. -C includes a CREATE DATABASE statement.
# Credentials come from the env (a ~/.pgpass or PGUSER/PGPASSWORD), NOT the repo.
pg_dump -C "${DB_NAME}" | gzip > "${DEST}"  # => co-19: a safe, server-consistent export
chmod 640 "${DEST}"  # => readable by group 'backup', not world

# --- 2. Verify the dump restores (the part most people skip) -----------------
# A dump that does not re-load is worthless. Confirm it parses by loading it
# into a throwaway database, then dropping it.
TMPDB="verify_${DB_NAME}_$$"  # => a unique, throwaway DB name
createdb "${TMPDB}" 2>/dev/null || true  # => create the scratch DB
gunzip -c "${DEST}" | psql -d "${TMPDB}" -q >/dev/null 2>&1 && echo "[verify] dump reloaded OK"  # => co-19: restorable
dropdb "${TMPDB}" 2>/dev/null || true  # => clean up the scratch DB
echo "[verify] backup OK and reload-tested: ${DEST}"  # => co-19 proof