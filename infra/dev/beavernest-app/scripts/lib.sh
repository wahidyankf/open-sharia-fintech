#!/usr/bin/env bash
# Shared readonly validation helpers for BeaverNest operational scripts.

beavernest_fail() {
	printf '%s\n' "$1" >&2
	return 1
}

beavernest_has_symlink_component() {
	local beavernest_path=$1
	local beavernest_component=$beavernest_path

	while [[ "$beavernest_component" != / && "$beavernest_component" != . ]]; do
		[[ -L "$beavernest_component" ]] && return 0
		beavernest_component=$(dirname -- "$beavernest_component")
	done

	return 1
}

beavernest_canonical_existing_directory() {
	local beavernest_path=$1
	[[ -n "$beavernest_path" && -d "$beavernest_path" && ! -L "$beavernest_path" ]] || return 1
	local beavernest_canonical
	beavernest_canonical=$(cd -P -- "$beavernest_path" && pwd -P) || return 1
	beavernest_has_symlink_component "$beavernest_canonical" && return 1
	printf '%s\n' "$beavernest_canonical"
}

beavernest_validate_safe_directory() {
	local beavernest_label=$1
	local beavernest_path=$2
	local beavernest_repository_root=$3
	local beavernest_canonical
	beavernest_canonical=$(beavernest_canonical_existing_directory "$beavernest_path") ||
		beavernest_fail "$beavernest_label must be an existing non-symlink directory" || return 1

	local beavernest_home
	beavernest_home=$(cd -P -- "$HOME" && pwd -P)
	[[ "$beavernest_canonical" != / && "$beavernest_canonical" != "$beavernest_home" && "$beavernest_canonical" != "$beavernest_repository_root" ]] ||
		beavernest_fail "$beavernest_label is not an allowed directory" || return 1

	case "$beavernest_canonical" in
	"$beavernest_repository_root"/*)
		beavernest_fail "$beavernest_label is not an allowed directory"
		return 1
		;;
	esac

	case "$beavernest_repository_root" in
	"$beavernest_canonical"/*)
		beavernest_fail "$beavernest_label is not an allowed directory"
		return 1
		;;
	esac

	printf '%s\n' "$beavernest_canonical"
}

beavernest_validate_directory_mode() {
	local beavernest_label=$1
	local beavernest_path=$2
	local beavernest_mode
	beavernest_mode=$(stat -f '%Lp' "$beavernest_path" 2>/dev/null || stat -c '%a' "$beavernest_path")
	[[ "$beavernest_mode" == 700 ]] || beavernest_fail "$beavernest_label must have mode 0700"
}

beavernest_validate_operation_name() {
	local beavernest_name=$1
	[[ "$beavernest_name" =~ ^[A-Za-z0-9_-]+\.sqlite3$ ]] ||
		beavernest_fail 'operation name must be a basename ending in .sqlite3'
}
