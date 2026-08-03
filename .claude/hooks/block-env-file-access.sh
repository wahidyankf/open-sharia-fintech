#!/usr/bin/env bash
# PreToolUse guard: refuse Read/Write/Edit/MultiEdit on any .env* file except .env.example.
# Also provides best-effort Bash guard for direct .env* manipulation and git add/commit.
# Repo policy: guard-env-file-access
set -euo pipefail

input="$(cat)"
tool_name="$(printf '%s' "$input" | jq -r '.tool_name // empty')"

deny() {
	cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Repo policy (guard-env-file-access): agents may not directly read, write, or edit .env* files. Only .env.example is permitted directly. Use a project script under apps/|libs/|scripts/, or ask the user to make the change manually."}}
JSON
}

# ── File-tool branch (Read / Write / Edit / MultiEdit) ──────────────────────
if [[ "$tool_name" == "Read" || "$tool_name" == "Write" ||
	"$tool_name" == "Edit" || "$tool_name" == "MultiEdit" ]]; then
	file_path="$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')"
	[ -z "$file_path" ] && exit 0
	base="$(basename "$file_path")"
	case "$base" in
	.env.example) exit 0 ;;
	.env | .env.*) deny ;;
	esac
	exit 0
fi

# ── Bash branch (best-effort heuristic) ─────────────────────────────────────
if [[ "$tool_name" == "Bash" ]]; then
	cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"
	[ -z "$cmd" ] && exit 0

	# ALLOW: project script or package runner invocations (check before deny).
	# Store regex in variable to avoid multiline-split-into-args issue.
	re_allow='(^|[[:space:]])(bash|sh|node|python|ruby)[[:space:]]+\.?/?(apps|libs|scripts)/|(^|[[:space:]])\.?/?(apps|libs|scripts)/|(^|[[:space:]])(npm|npx|nx|pnpm|yarn|volta)[[:space:]]'
	if printf '%s' "$cmd" | grep -qE "$re_allow"; then
		exit 0
	fi

	# ALLOW: course/teaching fixtures under an app's published content tree, e.g.
	# apps/ayokoding-www/content/**/kata.env. These are curriculum material, never
	# real secrets. Matches absolute paths too. The char before `.env` must be
	# neither `/` nor `.`, so dotfile `.env` / `.env.local` stay denied even under
	# content/. See guard-env-file-access §9 content-fixture exclusion.
	re_content_env='apps/[^/[:space:]]+/content/[^[:space:]]*[^/.[:space:]]\.env([[:space:]]|$)'
	if printf '%s' "$cmd" | grep -qE "$re_content_env"; then
		exit 0
	fi

	# DENY: direct read of a real .env* file via common read commands.
	re_cat_deny='(cat|less|head|tail|grep)[[:space:]].*\.env[^e]|(cat|less|head|tail|grep)[[:space:]].*\.env$'
	if printf '%s' "$cmd" | grep -qE "$re_cat_deny"; then
		printf '%s' "$cmd" | grep -qE '\.env\.example' && exit 0
		deny
		exit 0
	fi

	# DENY: redirect write to a real .env* file.
	# The `[^[:space:]]*` prefix lets the guard see redirect targets written as a
	# path (`> /abs/path/.env`, `> apps/x/.env.local`), not only a bare `.env`.
	re_redirect_deny='>[[:space:]]*[^[:space:]]*\.env([^e.]|$)|>[[:space:]]*[^[:space:]]*\.env\.[^e]|tee[[:space:]]+[^[:space:]]*\.env'
	if printf '%s' "$cmd" | grep -qE "$re_redirect_deny"; then
		printf '%s' "$cmd" | grep -qE '\.env\.example' && exit 0
		deny
		exit 0
	fi

	# DENY: git add or git commit explicitly naming a real .env* file.
	re_git_deny='git[[:space:]]+(add|commit)[^|&;]*\.env([^e.]|$)|git[[:space:]]+(add|commit)[^|&;]*\.env\.[^e]'
	if printf '%s' "$cmd" | grep -qE "$re_git_deny"; then
		printf '%s' "$cmd" | grep -qE '\.env\.example' && exit 0
		deny
		exit 0
	fi

	exit 0
fi

exit 0
