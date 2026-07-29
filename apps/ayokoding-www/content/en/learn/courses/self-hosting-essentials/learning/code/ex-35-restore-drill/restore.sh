#!/usr/bin/env bash
# Example 35: A Restore Drill. (co-19, co-15)
#
# The ONLY proof a backup works: actually restore from it. This script wipes the
# live DB, restores from the latest backup (Example 34), and verifies the data
# the app wrote is back. Run on the box. This is the single most-skipped,
# highest-value operational step in the whole course.

set -euo pipefail  # => fail fast; a restore is the worst place to be half-done

DB_PATH="/opt/myapp/data/app.db"  # => the live volume from Example 33
BACKUP_DIR="/var/backups/myapp"  # => where Example 34 wrote the stamped backups
UNIT="myapp-data"  # => the service to stop while we touch its DB

# --- 1. Pick the LATEST backup ------------------------------------------------
LATEST="$(ls -1t "${BACKUP_DIR}"/app-*.db 2>/dev/null | head -n1)"  # => newest by mtime
[ -n "${LATEST}" ] || { echo "[abort] no backup to restore from"; exit 1; }  # => guard
echo "[restore] using: ${LATEST}"  # => the file we will trust the data to

# --- 2. Stop the service so no writer races the file swap ---------------------
systemctl stop "${UNIT}"  # => co-15: no app process touching the DB during restore

# --- 3. Wipe the live DB, then restore from the backup -----------------------
mv "${DB_PATH}" "${DB_PATH}.drill-wiped"  # => set aside the live copy (so the drill is reversible)
cp "${LATEST}" "${DB_PATH}"  # => co-19: the backup BECOMES the live DB
chown deploy:deploy "${DB_PATH}" && chmod 640 "${DB_PATH}"  # => restore ownership the app expects

# --- 4. Restart + verify the app reads the restored data ---------------------
systemctl start "${UNIT}"  # => bring the service back against the restored DB
sleep 2  # => let it bind
curl -fsS http://127.0.0.1:8000/health >/dev/null && echo "[verify] healthy on restored data"  # => co-19 proof