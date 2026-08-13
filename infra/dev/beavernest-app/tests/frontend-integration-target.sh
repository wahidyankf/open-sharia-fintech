#!/usr/bin/env bash
set -euo pipefail

project_file="apps/beavernest-app/project.json"
test -f "$project_file"

unit_test_command="$(jq -er '.targets["test:unit"].options.command | strings' "$project_file")"

# Keep FVM's SDK lookup in the repository-local cache and make recovery from a
# corrupted local SDK non-interactive while forcing the Flutter subprocess to
# resolve that same selected SDK instead of any ambient checkout.
printf '%s\n' "$unit_test_command" | grep -Eq \
	'^CI=true[[:space:]]+FVM_CACHE_PATH=\.\./\.\./\.fvm-cache[[:space:]]+fvm[[:space:]]+install[[:space:]]+--skip-pub-get[[:space:]]*&&[[:space:]]+'
printf '%s\n' "$unit_test_command" | grep -Eq \
	'&&[[:space:]]+CI=true[[:space:]]+FVM_CACHE_PATH=\.\./\.\./\.fvm-cache[[:space:]]+FLUTTER_ROOT=\.\./\.\./\.fvm-cache/versions/3\.41\.5[[:space:]]+fvm[[:space:]]+flutter[[:space:]]+test[[:space:]]+test$'
