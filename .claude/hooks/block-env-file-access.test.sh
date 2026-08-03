#!/usr/bin/env bash
# Test suite for block-env-file-access.sh
# Run: bash .claude/hooks/block-env-file-access.test.sh
# Each assertion exits non-zero on failure (set -e propagates).
set -euo pipefail

HOOK=".claude/hooks/block-env-file-access.sh"
PASS=0
FAIL=0

assert_deny() {
	local desc="$1"
	local input="$2"
	local result
	result="$(printf '%s' "$input" | bash "$HOOK" 2>/dev/null || true)"
	if printf '%s' "$result" | jq -e '.hookSpecificOutput.permissionDecision=="deny"' >/dev/null 2>&1; then
		echo "PASS [DENY] $desc"
		PASS=$((PASS + 1))
	else
		echo "FAIL [DENY] $desc — got: $result"
		FAIL=$((FAIL + 1))
	fi
}

assert_allow() {
	local desc="$1"
	local input="$2"
	local result
	result="$(printf '%s' "$input" | bash "$HOOK" 2>/dev/null || true)"
	if [ -z "$result" ]; then
		echo "PASS [ALLOW] $desc"
		PASS=$((PASS + 1))
	else
		echo "FAIL [ALLOW] $desc — expected empty output, got: $result"
		FAIL=$((FAIL + 1))
	fi
}

echo "=== File-tool branch ==="

# DENY: Read on real .env file
assert_deny "Read .env.local" \
	'{"tool_name":"Read","tool_input":{"file_path":".env.local"}}'

# DENY: Write on nested real .env file
assert_deny "Write apps/organiclever-web/.env.local" \
	'{"tool_name":"Write","tool_input":{"file_path":"apps/organiclever-web/.env.local"}}'

# DENY: Edit on .env.production
assert_deny "Edit .env.production" \
	'{"tool_name":"Edit","tool_input":{"file_path":".env.production"}}'

# DENY: Write on arbitrary .env name
assert_deny "Write .env.whatever" \
	'{"tool_name":"Write","tool_input":{"file_path":".env.whatever"}}'

# ALLOW: Read on .env.example
assert_allow "Read .env.example" \
	'{"tool_name":"Read","tool_input":{"file_path":".env.example"}}'

# ALLOW: Write on nested .env.example
assert_allow "Write infra/dev/ose-web/.env.example" \
	'{"tool_name":"Write","tool_input":{"file_path":"infra/dev/ose-web/.env.example"}}'

echo ""
echo "=== Bash branch ==="

# DENY: cat .env.local
assert_deny "Bash: cat .env.local" \
	'{"tool_name":"Bash","tool_input":{"command":"cat .env.local"}}'

# DENY: echo redirect to .env.local
assert_deny "Bash: echo X > .env.local" \
	'{"tool_name":"Bash","tool_input":{"command":"echo X > .env.local"}}'

# DENY: git add .env.local
assert_deny "Bash: git add .env.local" \
	'{"tool_name":"Bash","tool_input":{"command":"git add .env.local"}}'

# ALLOW: cat .env.example
assert_allow "Bash: cat .env.example" \
	'{"tool_name":"Bash","tool_input":{"command":"cat .env.example"}}'

# ALLOW: project script invocation
assert_allow "Bash: bash scripts/setup-env.sh" \
	'{"tool_name":"Bash","tool_input":{"command":"bash scripts/setup-env.sh"}}'

# ALLOW: node script under apps/
assert_allow "Bash: node apps/foo/seed-env.js" \
	'{"tool_name":"Bash","tool_input":{"command":"node apps/foo/seed-env.js"}}'

# ALLOW: npm runner
assert_allow "Bash: npm run setup:env" \
	'{"tool_name":"Bash","tool_input":{"command":"npm run setup:env"}}'

echo ""
echo "=== Content-fixture exclusion (guard-env-file-access §9) ==="

# ALLOW: course fixture named <word>.env under an app content tree, absolute path
assert_allow "Bash: cat absolute apps/<app>/content/**/kata.env" \
	'{"tool_name":"Bash","tool_input":{"command":"cat /Users/x/repo/apps/ayokoding-www/content/en/learn/courses/self-hosting-essentials/drilling/code/kata-04-secret-committed-to-repo/after/kata.env"}}'

# ALLOW: same fixture reached through a worktree checkout
assert_allow "Bash: cat worktree apps/<app>/content/**/app.env" \
	'{"tool_name":"Bash","tool_input":{"command":"cat /Users/x/repo/worktrees/wt/apps/ayokoding-www/content/en/learn/courses/self-hosting-essentials/learning/code/ex-15-env-config/app.env"}}'

# ALLOW: writing a course fixture (authoring curriculum material)
assert_allow "Bash: redirect into apps/<app>/content/**/kata.env" \
	'{"tool_name":"Bash","tool_input":{"command":"echo FOO=bar > /Users/x/repo/apps/ayokoding-www/content/en/c/kata.env"}}'

# ALLOW: Read tool on a course fixture
assert_allow "Read apps/<app>/content/**/kata.env" \
	'{"tool_name":"Read","tool_input":{"file_path":"/Users/x/repo/apps/ayokoding-www/content/en/c/kata.env"}}'

# DENY: dotfile .env under a content tree is NOT a fixture — still a real env file
assert_deny "Bash: cat apps/<app>/content/**/.env (dotfile)" \
	'{"tool_name":"Bash","tool_input":{"command":"cat /Users/x/repo/apps/ayokoding-www/content/en/c/.env"}}'

# DENY: dotfile .env.local under a content tree
assert_deny "Read apps/<app>/content/**/.env.local (dotfile)" \
	'{"tool_name":"Read","tool_input":{"file_path":"/Users/x/repo/apps/ayokoding-www/content/en/c/.env.local"}}'

# DENY: a <word>.env file OUTSIDE any content tree gets no exclusion
assert_deny "Bash: cat apps/<app>/src/secrets.env (not under content/)" \
	'{"tool_name":"Bash","tool_input":{"command":"cat /Users/x/repo/apps/ose-be/src/secrets.env"}}'

# DENY: absolute-path redirect into a real .env (regression — the guard used to
# only see a bare `> .env`, missing any path-prefixed redirect target)
assert_deny "Bash: echo X > /abs/path/.env.local" \
	'{"tool_name":"Bash","tool_input":{"command":"echo X > /Users/x/repo/apps/ose-be/.env.local"}}'

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ]
