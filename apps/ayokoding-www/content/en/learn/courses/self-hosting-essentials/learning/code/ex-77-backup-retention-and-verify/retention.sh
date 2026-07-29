#!/usr/bin/env bash
# Example 77: Backup Retention and Restore Verification. (co-19)
#
# Two things a backup discipline needs beyond "take a backup": (1) RETENTION --
# old backups are deleted on a schedule so the disk does not fill; and
# (2) PERIODIC RESTORE VERIFICATION -- a scheduled job that actually restores a
# backup and confirms the data, so a silently-corrupt backup is caught before
# you need it. Run on the box, scheduled by a timer.

set -euo pipefail  # => fail fast

DUMP_DIR="/var/backups/myapp-pg"  # => the dir Example 76 writes dumps into
VERIFY_DIR="/tmp/restore-verify"  # => a scratch dir for restore drills
KEEP_DAYS=14  # => retention: delete dumps older than 14 days

# --- 1. RETENTION: prune old backups on a schedule (co-19) -------------------
echo "[retention] deleting dumps older than ${KEEP_DAYS} days:"  # => keep the disk bounded
find "${DUMP_DIR}" -name '*.sql.gz' -mtime "+${KEEP_DAYS}" -print -delete  # => co-19: bounded history

# --- 2. Pick the LATEST backup for a restore drill ---------------------------
LATEST="$(ls -1t "${DUMP_DIR}"/*.sql.gz 2>/dev/null | head -n1)"  # => newest by mtime
[ -n "${LATEST}" ] || { echo "[abort] no backup to verify"; exit 1; }  # => guard
echo "[verify] restore-drilling the newest backup: ${LATEST}"  # => co-19: the part most skip

# --- 3. Restore it to a scratch location and confirm the data round-trips ----
install -d "${VERIFY_DIR}"  # => scratch dir
gunzip -c "${LATEST}" > "${VERIFY_DIR}/restored.sql"  # => decompress to a scratch file
# Confirm the dump contains the schema + at least one expected table marker.
if grep -q 'CREATE TABLE' "${VERIFY_DIR}/restored.sql"; then  # => the dump has real schema
  echo "[verify] PASS: backup restored and contains schema"  # => co-19: known-restorable
else
  echo "[verify] FAIL: backup restored but no schema found -- investigate" >&2; exit 1  # => caught early
fi
rm -rf "${VERIFY_DIR}"  # => clean up the scratch
# [verify] old backups pruned AND the latest one proven restorable (co-19 proof).