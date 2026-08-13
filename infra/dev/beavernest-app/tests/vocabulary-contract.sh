#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/assertions.bash"

jq -e '.tags | index("platform:flutter")' apps/beavernest-app/project.json >/dev/null
grep -Fq 'Flutter Web' apps/beavernest-app/README.md
assert_no_match git grep -Eq -- 'vite|react' -- apps/beavernest-app apps/beavernest-app-e2e
