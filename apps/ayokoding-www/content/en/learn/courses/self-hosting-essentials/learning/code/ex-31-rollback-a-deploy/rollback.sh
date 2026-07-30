#!/usr/bin/env bash
# Example 31: Roll Back a Deploy. (co-16, co-18)
#
# A bad deploy happens. A PaaS keeps a history of releases, so "go back to the
# last known-good one" is ONE command -- the operational payoff of co-16's
# build history. Run on the box when a push misbehaves.

set -euo pipefail  # => fail fast; a rollback that silently no-ops is worse than an error

APP_NAME="myapp"  # => the deployed app

# --- 1. List recent releases (each push = one release) ------------------------
echo "[history] recent releases of ${APP_NAME}:"  # => co-16: the build history a rollback reads from
dokku releases:list "${APP_NAME}"  # => numbered list, newest last (e.g. v1 .. v5)

# --- 2. Identify the last known-good version ----------------------------------
# (Inspect the list, pick the version BEFORE the bad push.)
ROLLBACK_TO="${1:-vN}"  # => pass the target version as $1; placeholder if omitted
echo "[rollback] target: ${ROLLBACK_TO}"  # => the version to return to

# --- 3. Roll back to it -------------------------------------------------------
dokku tags:deploy "${APP_NAME}" "${ROLLBACK_TO}" 2>/dev/null || dokku ps:rollback "${APP_NAME}"  # => restore that release's image
echo "[verify] the OLD version is now serving:"  # => co-16/co-18 proof
echo "  curl -s https://${APP_NAME}.<domain>/version   # => the previous version string"  # => rollback confirmed