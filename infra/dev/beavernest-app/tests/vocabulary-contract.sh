#!/usr/bin/env bash
set -euo pipefail

jq -e '.tags | index("platform:flutter")' apps/beavernest-app/project.json >/dev/null
grep -Fq 'Flutter Web' apps/beavernest-app/README.md
! grep -Eq 'vite|react' apps/beavernest-app apps/beavernest-app-e2e
