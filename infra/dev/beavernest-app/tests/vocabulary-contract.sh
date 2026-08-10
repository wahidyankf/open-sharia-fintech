#!/usr/bin/env bash
set -euo pipefail

jq -e '.tags | index("platform:vite")' apps/beavernest-app-web/project.json >/dev/null
rg -Fq 'Static `dist/` production build' apps/beavernest-app-web/README.md
rg -Fq 'BeaverNest Vite/React app client' docs/reference/monorepo-structure.md
! rg -q 'beavernest-app-web.*Next\.js|beavernest-app-web.*\.next' AGENTS.md apps/beavernest-app-web docs/reference/monorepo-structure.md repo-governance/development/infra/nx-targets.md
