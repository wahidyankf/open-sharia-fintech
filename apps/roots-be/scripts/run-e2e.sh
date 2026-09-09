#!/usr/bin/env bash
# E2E test runner for roots-be.
#
# The service owns no local-resource boundary -- no database, no message broker, no disk -- so
# unlike apps/ose-be/scripts/run-e2e.sh there is no docker-compose stack to bring up. This script
# builds the binary and hands process lifecycle to the Playwright harness, which starts and stops
# it inside scenario steps so startup behaviour stays observable.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

# Fail fast, before paying for a build, on any unconditional test.skip() left in the suite.
# test.skip(condition, reason) -- the documented Playwright environment-guard form -- is
# intentionally allowed through.
if grep -rn -E --include='*.ts' --exclude-dir=node_modules --exclude-dir=.features-gen \
	--exclude-dir=test-results --exclude-dir=playwright-report \
	'\$?test\.skip\([^,)]*\)' "${ROOT}/apps/roots-be-e2e"; then
	echo "ERROR: unconditional test.skip() found in the files above - use test.skip(condition, reason) for a legitimate environment guard, or remove it" >&2
	exit 1
fi

# Build through Nx so codegen runs first and the binary matches the current contract.
npm exec -- nx run roots-be:build

cd "${ROOT}/apps/roots-be-e2e"
npx bddgen && npx playwright test
