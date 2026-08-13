#!/usr/bin/env bash
set -euo pipefail

project_file="apps/beavernest-app/project.json"
test -f "$project_file"

unit_test_command="$(jq -er '.targets["test:unit"].options.command | strings' "$project_file")"

# Keep FVM's SDK lookup in the repository-local cache for both setup and test execution.
printf '%s\n' "$unit_test_command" | grep -Eq \
\t'^FVM_CACHE_PATH=\.\./\.\./\.fvm-cache[[:space:]]+fvm[[:space:]]+install[[:space:]]+--skip-pub-get[[:space:]]*&&[[:space:]]+'
printf '%s\n' "$unit_test_command" | grep -Eq \
\t'&&[[:space:]]+FVM_CACHE_PATH=\.\./\.\./\.fvm-cache[[:space:]]+fvm[[:space:]]+flutter[[:space:]]+test[[:space:]]+test$'
