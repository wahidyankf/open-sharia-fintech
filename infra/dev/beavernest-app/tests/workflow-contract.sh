#!/usr/bin/env bash
set -euo pipefail

rg -Fq 'subosito/flutter-action@v2' .github/workflows/beavernest-app-test-local-deploy-stag.yml
rg -Fq 'beavernest-app-e2e:test:e2e' .github/workflows/beavernest-app-test-local-deploy-stag.yml
rg -Fq 'beavernest-app:lint' .github/workflows/beavernest-app-test-local-deploy-stag.yml
! test -e .github/workflows/beavernest-app-test-stag.yml
! rg -q 'beavernest-app-web|Vercel preview|localhost:19320' .github/workflows/beavernest-app-test-local-deploy-stag.yml
