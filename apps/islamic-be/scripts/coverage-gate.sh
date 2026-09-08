#!/usr/bin/env bash
# Enforce the Unit line-coverage floor over islamic-be's production denominator.
#
# The denominator is ./internal/... only. Two exclusions, both deliberate:
#
#   cmd/islamic-be      -- binds a socket and reads the process environment, the
#                          exact boundaries Unit proof may not touch. It holds no
#                          decisions; every branch it could have lives in
#                          internal/config and internal/router, both at 100%.
#   generated-contracts -- emitted by oapi-codegen from the OpenAPI document.
#                          Not authored here, and rewritten on every codegen run.
#
# Neither exclusion hides retained production behaviour: the router registers the
# generated handlers and is itself covered, so a contract route that stopped
# being served would fail internal/router's tests.
set -euo pipefail

app_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
minimum="${COVERAGE_MINIMUM:-99}"

cd "$app_dir"

go test ./internal/... -coverprofile=cover.out -covermode=atomic

total="$(go tool cover -func=cover.out | awk '$1 == "total:" { sub(/%/, "", $3); print $3 }')"

if [ -z "$total" ]; then
	echo "coverage-gate: could not read a total from cover.out" >&2
	exit 1
fi

# awk rather than shell arithmetic: the total is fractional.
if awk -v t="$total" -v m="$minimum" 'BEGIN { exit !(t < m) }'; then
	echo "coverage-gate: FAIL - ${total}% is below the ${minimum}% floor" >&2
	exit 1
fi

echo "coverage-gate: PASS - ${total}% meets the ${minimum}% floor"
