#!/usr/bin/env bash
# Example 34: A Scripted Tested Backup of the Data. (co-19)
#
# An untested backup is a wish. This script takes a consistent copy of the
# service's SQLite DB (using sqlite3's `.backup`, which is safe against a
# running writer), stamps it, and immediately VERIFIES the copy opens -- so the
# backup is proven restorable at the moment it is taken. Run on the box (and
# schedule it via a timer, Example 47).

set -euo pipefail  # => fail fast; a silent backup failure is the worst kind

DB_PATH="/opt/myapp/data/app.db"  # => the volume from Example 33
BACKUP_DIR="/var/backups/myapp"  # => a dedicated, app-specific backup location
install -d -m 750 "${BACKUP_DIR}"  # => ensure the dir exists with sane perms

# --- 1. Take a CONSISTENT snapshot (safe while the app is writing) ------------
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"  # => UTC ISO-8601-ish stamp; sortable + unambiguous
DEST="${BACKUP_DIR}/app-${STAMP}.db"  # => one file per backup, named by time
sqlite3 "${DB_PATH}" ".backup '${DEST}'"  # => co-19: sqlite's online backup API -> no torn writes
chmod 640 "${DEST}"  # => readable by group 'backup', not world-readable

# --- 2. TEST the backup at backup time (the part most people skip) ------------
if ! sqlite3 "${DEST}" 'PRAGMA integrity_check;' | grep -q '^ok$'; then  # => opens + passes a checksum
  echo "[FAIL] backup ${DEST} failed integrity check" >&2  # => a corrupt backup is no backup
  exit 1
fi
echo "[verify] backup OK and integrity-checked: ${DEST}"  # => co-19: proven restorable NOW
echo "[next]  Example 35 wipes the DB and restores from this file"  # => the drill that finishes the proof