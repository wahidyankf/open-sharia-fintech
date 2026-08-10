#!/usr/bin/env bash

# Validate persistent storage before the unprivileged application starts. The
# image account is intentionally stable so an operator can prepare the bind
# source without granting the container broader host access.
set -euo pipefail

readonly beavernest_expected_owner='10001:10001'
readonly beavernest_directory_mode='700'
readonly beavernest_file_mode='600'

fail() {
	printf 'container-entrypoint: %s\n' "$1" >&2
	exit 1
}

stat_owner() {
	/usr/bin/stat --format='%u:%g' -- "$1"
}

stat_mode() {
	/usr/bin/stat --format='%a' -- "$1"
}

validate_owner() {
	local beavernest_path="$1"

	[[ "$(stat_owner "$beavernest_path")" == "$beavernest_expected_owner" ]] ||
		fail "unsafe ownership: $beavernest_path must be owned by $beavernest_expected_owner"
}

validate_mode() {
	local beavernest_path="$1"
	local beavernest_expected_mode="$2"

	[[ "$(stat_mode "$beavernest_path")" == "$beavernest_expected_mode" ]] ||
		fail "unsafe mode: $beavernest_path must have mode $beavernest_expected_mode"
}

validate_directory_tree() {
	local beavernest_directory="$1"
	local beavernest_path=''

	[[ -d "$beavernest_directory" ]] || fail "data directory does not exist: $beavernest_directory"
	[[ ! -L "$beavernest_directory" ]] || fail "data directory must not be a symlink: $beavernest_directory"
	[[ -w "$beavernest_directory" ]] || fail "data directory is not writable: $beavernest_directory"
	validate_owner "$beavernest_directory"
	validate_mode "$beavernest_directory" "$beavernest_directory_mode"

	while IFS= read -r -d '' beavernest_path; do
		[[ ! -L "$beavernest_path" ]] || fail "persistent storage must not contain symlinks: $beavernest_path"
		validate_owner "$beavernest_path"

		if [[ -d "$beavernest_path" ]]; then
			validate_mode "$beavernest_path" "$beavernest_directory_mode"
		elif [[ -f "$beavernest_path" ]]; then
			validate_mode "$beavernest_path" "$beavernest_file_mode"
		else
			fail "persistent storage contains unsupported path type: $beavernest_path"
		fi
	done < <(/usr/bin/find -P "$beavernest_directory" -mindepth 1 -print0)
}

umask 0077

readonly beavernest_data_directory="${BEAVERNEST_BE_DATA_DIRECTORY:-/var/lib/beavernest}"
validate_directory_tree "$beavernest_data_directory"

if [[ -n "${BEAVERNEST_BE_BACKUP_DIRECTORY:-}" ]]; then
	validate_directory_tree "$BEAVERNEST_BE_BACKUP_DIRECTORY"
fi

exec "$@"
