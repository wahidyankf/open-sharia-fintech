#!/usr/bin/env bash
set -euo pipefail

rg -Fq 'beavernest-be | beavernest-app-web) echo "build-beavernest-be=true"' .github/workflows/publish-images.yml
rg -Fq 'Combined same-origin E2E' .github/workflows/_reusable-app-test-local-deploy-stag.yml
rg -Fq 'test:e2e:runner' .github/workflows/_reusable-app-test-local-deploy-stag.yml
rg -Fq 'BEAVERNEST_BE_PUBLIC_PORT=19300' .github/workflows/_reusable-app-test-local-deploy-stag.yml
! test -e .github/workflows/beavernest-app-test-stag.yml
! rg -q 'stag-beavernest-app-web|Vercel preview|localhost:19320' .github/workflows/beavernest-app-test-local-deploy-stag.yml .github/workflows/_reusable-app-test-local-deploy-stag.yml
