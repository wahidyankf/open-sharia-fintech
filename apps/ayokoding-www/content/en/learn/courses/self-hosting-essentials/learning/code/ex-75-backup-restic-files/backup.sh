#!/usr/bin/env bash
# Example 34 took a SQLite backup with sqlite3 .backup. Example 75 uses RESTIC,
# a deduplicating backup tool: it snapshots a DIRECTORY, dedups across runs
# (so daily snapshots of a mostly-unchanged tree are cheap), and supports
# encrypted remote repos. This is the "grows beyond one file" backup. Run on
# the box, scheduled by a timer (Example 47's shape).

set -euo pipefail  # => fail fast; a silent backup failure is the worst kind

REPO="/srv/restic/myapp"  # => a local restic repo (point this at a remote/NFS path for off-site)
DATA_DIR="/opt/myapp/data"  # => the volume from Example 33 (the thing worth backing up)

# --- 1. Initialize the repo once (idempotent: skip if already initialized) ----
RESTIC_PASSWORD="${RESTIC_PASSWORD:?set RESTIC_PASSWORD in the env}"  # => co-13: the repo key, out of band
restic -r "${REPO}" snapshots >/dev/null 2>&1 || restic -r "${REPO}" init  # => init only if empty

# --- 2. Take a snapshot (deduplicated, so cheap on a stable tree) ------------
restic -r "${REPO}" backup "${DATA_DIR}" --tag myapp  # => co-19: one timestamped, deduped snapshot
# restic only stores the BLOCKS that changed since the last snapshot -> a daily
# backup of a 1GB tree with 10MB of daily churn stores ~10MB, not 1GB, per run.

# --- 3. Forget old snapshots per a retention policy (Example 77 expands) -----
restic -r "${REPO}" forget --keep-daily 7 --keep-weekly 4 --prune  # => keep 7 dailies + 4 weeklies

# --- Verify ------------------------------------------------------------------
restic -r "${REPO}" snapshots  # => lists each snapshot with a time + ID
echo "[verify] snapshots present; 'restic -r ${REPO} restore <id> --target /tmp/x' reproduces the tree (co-19)"