#!/usr/bin/env bash
# Test suite for block-env-file-access.sh
# Usage: bash .claude/hooks/block-env-file-access.test.sh
set -euo pipefail

HOOK=".claude/hooks/block-env-file-access.sh"
PASS=0
FAIL=0

assert_deny() {
	local label="$1"
	local input="$2"
	local output
	output="$(printf '%s' "$input" | bash "$HOOK")"
	if printf '%s' "$output" | jq -e '.hookSpecificOutput.permissionDecision=="deny"' >/dev/null 2>&1; then
		echo "PASS [DENY] $label"
		PASS=$((PASS + 1))
	else
		echo "FAIL [DENY] $label — expected deny, got: $output"
		FAIL=$((FAIL + 1))
	fi
}

assert_allow() {
	local label="$1"
	local input="$2"
	local output
	output="$(printf '%s' "$input" | bash "$HOOK")"
	if [ -z "$output" ]; then
		echo "PASS [ALLOW] $label"
		PASS=$((PASS + 1))
	else
		echo "FAIL [ALLOW] $label — expected empty output, got: $output"
		FAIL=$((FAIL + 1))
	fi
}

# File-tool ALLOW cases — named-file rule: only .env.prod / .env.stag are restricted.
assert_allow "Read .env" \
	'{"tool_name":"Read","tool_input":{"file_path":".env"}}'

assert_allow "Read .env.local" \
	'{"tool_name":"Read","tool_input":{"file_path":".env.local"}}'

assert_allow "Read .env.test" \
	'{"tool_name":"Read","tool_input":{"file_path":".env.test"}}'

assert_allow "Write apps/coralpolyp-be/.env.local" \
	'{"tool_name":"Write","tool_input":{"file_path":"apps/coralpolyp-be/.env.local"}}'

assert_allow "Edit .env.production" \
	'{"tool_name":"Edit","tool_input":{"file_path":".env.production"}}'

assert_allow "Write .env.whatever" \
	'{"tool_name":"Write","tool_input":{"file_path":".env.whatever"}}'

assert_allow "Read .env.example" \
	'{"tool_name":"Read","tool_input":{"file_path":".env.example"}}'

assert_allow "Write apps/coralpolyp-fe/.env.example" \
	'{"tool_name":"Write","tool_input":{"file_path":"apps/coralpolyp-fe/.env.example"}}'

# File-tool DENY cases — the two restricted tiers, across Read/Edit/Write.
assert_deny "Read .env.prod" \
	'{"tool_name":"Read","tool_input":{"file_path":".env.prod"}}'

assert_deny "Edit .env.prod" \
	'{"tool_name":"Edit","tool_input":{"file_path":".env.prod"}}'

assert_deny "Write .env.prod" \
	'{"tool_name":"Write","tool_input":{"file_path":".env.prod"}}'

assert_deny "Read .env.stag" \
	'{"tool_name":"Read","tool_input":{"file_path":".env.stag"}}'

assert_deny "Edit .env.stag" \
	'{"tool_name":"Edit","tool_input":{"file_path":".env.stag"}}'

assert_deny "Write .env.stag" \
	'{"tool_name":"Write","tool_input":{"file_path":".env.stag"}}'

# Bash ALLOW cases — named-file rule.
assert_allow "Bash cat .env.example" \
	'{"tool_name":"Bash","tool_input":{"command":"cat .env.example"}}'

assert_allow "Bash bash scripts/setup-env.sh" \
	'{"tool_name":"Bash","tool_input":{"command":"bash scripts/setup-env.sh"}}'

assert_allow "Bash cargo run apps/rhino-cli" \
	'{"tool_name":"Bash","tool_input":{"command":"cargo run --manifest-path apps/rhino-cli/Cargo.toml"}}'

assert_allow "Bash npm run setup:env" \
	'{"tool_name":"Bash","tool_input":{"command":"npm run setup:env"}}'

assert_allow "Bash cat .env.local" \
	'{"tool_name":"Bash","tool_input":{"command":"cat .env.local"}}'

assert_allow "Bash echo > .env.local" \
	'{"tool_name":"Bash","tool_input":{"command":"echo X > .env.local"}}'

assert_allow "Bash git add .env.local" \
	'{"tool_name":"Bash","tool_input":{"command":"git add .env.local"}}'

# Bash DENY cases — the two restricted tiers only.
assert_deny "Bash cat .env.prod" \
	'{"tool_name":"Bash","tool_input":{"command":"cat .env.prod"}}'

assert_deny "Bash head -5 infra/x/.env.prod" \
	'{"tool_name":"Bash","tool_input":{"command":"head -5 infra/x/.env.prod"}}'

assert_deny "Bash cp .env.stag /tmp/x" \
	'{"tool_name":"Bash","tool_input":{"command":"cp .env.stag /tmp/x"}}'

assert_deny "Bash echo K=v > .env.prod" \
	'{"tool_name":"Bash","tool_input":{"command":"echo K=v > .env.prod"}}'

assert_deny "Bash git add .env.prod" \
	'{"tool_name":"Bash","tool_input":{"command":"git add .env.prod"}}'

# Regression: ALLOW_PATTERN must not let a restricted-tier target under apps/|libs/|scripts/
# bypass the deny checks — this is the realistic case, since real env files live under apps/.
assert_deny "Bash redirect apps/-path .env.prod (ALLOW_PATTERN bypass regression)" \
	'{"tool_name":"Bash","tool_input":{"command":"printf X > apps/rhino-cli/.env.prod"}}'

assert_deny "Bash cat apps/-path .env.prod (ALLOW_PATTERN bypass regression)" \
	'{"tool_name":"Bash","tool_input":{"command":"cat apps/rhino-cli/.env.prod"}}'

assert_deny "Bash git add libs/-path .env.stag (ALLOW_PATTERN bypass regression)" \
	'{"tool_name":"Bash","tool_input":{"command":"git add libs/x/.env.stag"}}'

# Content-fixture exclusion (guard-env-file-access §9) — regression pins.
# Course fixtures named <word>.env under apps/<app>/content/** are curriculum
# material, never real secrets; allowed under both the old and new policy.
assert_allow "Bash cat apps/<app>/content/**/kata.env" \
	'{"tool_name":"Bash","tool_input":{"command":"cat /r/apps/ayokoding-www/content/en/c/kata.env"}}'

assert_allow "Bash cat worktree apps/<app>/content/**/app.env" \
	'{"tool_name":"Bash","tool_input":{"command":"cat /r/worktrees/wt/apps/ayokoding-www/content/en/c/app.env"}}'

assert_allow "Bash redirect into apps/<app>/content/**/kata.env" \
	'{"tool_name":"Bash","tool_input":{"command":"echo FOO=bar > /r/apps/ayokoding-www/content/en/c/kata.env"}}'

assert_allow "Read apps/<app>/content/**/kata.env" \
	'{"tool_name":"Read","tool_input":{"file_path":"/r/apps/ayokoding-www/content/en/c/kata.env"}}'

# Formerly-denied dotfile/near-.env cases — now allowed too, since only
# .env.prod / .env.stag are restricted anywhere under the named-file rule.
assert_allow "Bash cat apps/<app>/content/**/.env (dotfile)" \
	'{"tool_name":"Bash","tool_input":{"command":"cat /r/apps/ayokoding-www/content/en/c/.env"}}'

assert_allow "Read apps/<app>/content/**/.env.local (dotfile)" \
	'{"tool_name":"Read","tool_input":{"file_path":"/r/apps/ayokoding-www/content/en/c/.env.local"}}'

assert_allow "Bash cat apps/<app>/src/secrets.env (not a restricted tier)" \
	'{"tool_name":"Bash","tool_input":{"command":"cat /r/apps/coralpolyp-be/src/secrets.env"}}'

assert_allow "Bash echo X > /abs/path/.env.local" \
	'{"tool_name":"Bash","tool_input":{"command":"echo X > /r/apps/coralpolyp-be/.env.local"}}'

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
