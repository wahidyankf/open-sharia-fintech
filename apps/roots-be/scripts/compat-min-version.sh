#!/usr/bin/env bash
# Assert that go.mod's `go` directive still matches the pinned floor.
#
# This is a real check, not an echo. Go has a genuine minimum-version
# declaration, so asserting it costs nothing and keeps roots-be out of the set
# of stub targets that plans/backlog/remove-stale-compat-min-version-stubs wants
# removed. The pin is duplicated here on purpose: if it were read from go.mod it
# would assert only that go.mod equals itself.
set -euo pipefail

expected="1.26"

app_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
actual="$(awk '$1 == "go" { print $2; exit }' "$app_dir/go.mod")"

if [ "$actual" != "$expected" ]; then
	echo "compat:min-version: FAIL - go.mod declares go ${actual:-<none>}, expected ${expected}" >&2
	exit 1
fi

echo "compat:min-version: PASS - go.mod declares go ${actual}"
