#!/usr/bin/env bash
set -euo pipefail

jq -e '.tags | index("platform:flutter")' apps/beavernest-app/project.json >/dev/null
rg -Fq 'Flutter Web' apps/beavernest-app/README.md
! rg -q 'vite|react' apps/beavernest-app apps/beavernest-app-e2e
