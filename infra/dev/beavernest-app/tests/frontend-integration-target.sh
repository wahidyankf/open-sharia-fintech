#!/usr/bin/env bash
set -euo pipefail

project_file="apps/beavernest-app-web/project.json"
test -f "$project_file"
jq -e '.targets["test:integration"].cache == false' "$project_file" >/dev/null
jq -e '.targets["test:integration"].options.command | contains("vitest run --config vitest.integration.config.ts")' "$project_file" >/dev/null
