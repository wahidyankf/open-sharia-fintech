#!/usr/bin/env bash
set -euo pipefail

project_file="apps/beavernest-app/project.json"
test -f "$project_file"
jq -e '.targets["test:unit"].options.command == "fvm flutter test test"' "$project_file" >/dev/null
