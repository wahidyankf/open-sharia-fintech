#!/usr/bin/env bash
# PreToolUse guard: named-file rule — refuse Read/Write/Edit/MultiEdit and direct Bash
# manipulation of exactly .env.prod / .env.stag (the two restricted-secrets tiers). Every
# other real .env* file (.env, .env.local, .env.test, .env.example, ...) is agent-readable.
# Commit policy is unaffected and stays deny-all for every .env* file — see
# `apps/rhino-cli/src/commands/env_staged_guard.rs`'s `is_offending` (guard-env-file-access).
set -euo pipefail

# The two restricted tiers, shared by both branches below — adding a tier is a one-line change.
RESTRICTED_TIERS='prod|stag'

input="$(cat)"
tool_name="$(printf '%s' "$input" | jq -r '.tool_name // empty')"

# --- File-tool branch (Read/Write/Edit/MultiEdit) ---
if [ "$tool_name" != "Bash" ]; then
	file_path="$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')"
	[ -z "$file_path" ] && exit 0
	base="$(basename "$file_path")"
	if printf '%s' "$base" | grep -qE "^\\.env\\.($RESTRICTED_TIERS)\$"; then
		cat <<JSON
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Repo policy (guard-env-file-access): agents may not directly read, write, or edit .env.prod or .env.stag. Use a project script under apps/|libs/|scripts/, or ask the user to make the change manually."}}
JSON
	fi
	exit 0
fi

# --- Bash branch ---
cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"
[ -z "$cmd" ] && exit 0

# Check for direct .env.prod / .env.stag manipulation FIRST (named-file rule), before any
# allowlist — real env files live under apps/, so an allowlist keyed on "apps/" substrings
# must never be permitted to shadow a restricted-tier deny (that was a real bypass: a command
# like `cat apps/rhino-cli/.env.prod` matched the old apps/-prefix allow before deny ever ran).
# Check for targeted dangerous operations only (read-file commands, write
# redirections, git staging/commit) against exactly the two restricted tiers.
# Safe git queries (check-ignore, ls-files) and tool invocations with .env* in
# argument strings (e.g. jq filters) are intentionally NOT denied — best-effort guard.
deny_env() {
	cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Repo policy (guard-env-file-access): agents may not directly manipulate .env.prod or .env.stag via Bash. Invoke a project script under apps/|libs/|scripts/ instead, or ask the user to make the change manually."}}
JSON
	exit 0
}

RESTRICTED_TIER_PATTERN="\\.env\\.($RESTRICTED_TIERS)([^a-z]|\$)"

# Deny: write redirection targeting .env.prod or .env.stag.
printf '%s' "$cmd" | grep -qE "(>|>>)[[:space:]]*[^[:space:]]*$RESTRICTED_TIER_PATTERN" && deny_env

# Deny: read-file / copy / move commands with .env.prod or .env.stag as a bare argument.
printf '%s' "$cmd" | grep -qE "(^|[[:space:]])(cat|less|head|tail|more|tee|cp|mv|sed)[[:space:]].*$RESTRICTED_TIER_PATTERN" && deny_env

# Deny: git add/stage with .env.prod or .env.stag as a path argument.
# git commit is intentionally excluded — .env* in a commit message is not a file path;
# the pre-commit hook (`rhino-cli env staged-guard validate`) guards actual staged files.
printf '%s' "$cmd" | grep -qE "(^|[[:space:]])git[[:space:]]+(add|stage)[[:space:]].*$RESTRICTED_TIER_PATTERN" && deny_env

# Allow pattern: command references project tooling (apps/, libs/, scripts/) or package runners.
# Evaluated AFTER deny, so it can never shadow a restricted-tier match above.
ALLOW_PATTERN='(^|[[:space:]])(apps/|libs/|scripts/|\./scripts/|\./apps/|\./libs/|npm |npx |nx |cargo |volta run|pnpm |yarn )'

# If command references a path under apps/, libs/, scripts/ or a known package runner — allow.
if printf '%s' "$cmd" | grep -qE "$ALLOW_PATTERN"; then
	exit 0
fi

# Allow: course/teaching fixtures under an app's published content tree, e.g.
# apps/ayokoding-www/content/**/kata.env — curriculum material, never real secrets.
# Matches absolute paths too. The char before `.env` must be neither `/` nor `.`,
# so dotfile `.env` / `.env.local` stay denied even under content/.
# See guard-env-file-access §9 content-fixture exclusion.
CONTENT_FIXTURE_ALLOW='apps/[^/[:space:]]+/content/[^[:space:]]*[^/.[:space:]]\.env([[:space:]]|$)'
if printf '%s' "$cmd" | grep -qE "$CONTENT_FIXTURE_ALLOW"; then
	exit 0
fi

exit 0
