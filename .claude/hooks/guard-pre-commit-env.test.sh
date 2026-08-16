#!/usr/bin/env bash
# Self-test for the pre-commit staged-.env* guard (`env-staged-guard` in repo-config.yml).
# Run: bash .claude/hooks/guard-pre-commit-env.test.sh
# Green: exits 0 when the guard denies a real .env* and allows .env.example.
# The guard moved from scripts/check-no-env-staged.sh to the rhino-cli command below
# when the SDLC-parity plan replaced the inline shell script.
set -euo pipefail

GUARD_CMD=(cargo run --profile gate --quiet --manifest-path apps/rhino-cli/Cargo.toml -- env staged-guard validate)
PASS=0
FAIL=0

cleanup() {
	git restore --staged local-tmp/.env.local 2>/dev/null || true
	git restore --staged local-tmp/.env.example 2>/dev/null || true
	rm -f local-tmp/.env.local local-tmp/.env.example
}
trap cleanup EXIT

mkdir -p local-tmp

echo "=== Case 1: staged .env.local must be rejected ==="
printf 'SECRET=test\n' >local-tmp/.env.local
git add -f local-tmp/.env.local
guard_output="$("${GUARD_CMD[@]}" 2>&1 || true)"
if printf '%s' "$guard_output" | grep -q "ERROR"; then
	echo "PASS [DENY] staged .env.local rejected"
	PASS=$((PASS + 1))
else
	echo "FAIL [DENY] staged .env.local was not rejected (guard missing or did not output ERROR)"
	FAIL=$((FAIL + 1))
fi
git restore --staged local-tmp/.env.local
rm -f local-tmp/.env.local

echo "=== Case 2: staged .env.example must be allowed ==="
printf 'SECRET=changeme\n' >local-tmp/.env.example
git add -f local-tmp/.env.example
if "${GUARD_CMD[@]}"; then
	echo "PASS [ALLOW] staged .env.example allowed"
	PASS=$((PASS + 1))
else
	echo "FAIL [ALLOW] staged .env.example was rejected"
	FAIL=$((FAIL + 1))
fi
git restore --staged local-tmp/.env.example
rm -f local-tmp/.env.example

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ]
