#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/assertions.bash"

grep -Fq 'subosito/flutter-action@v2' .github/workflows/beavernest-app-test-local-deploy-stag.yml
grep -Fq 'beavernest-app-e2e:test:e2e' .github/workflows/beavernest-app-test-local-deploy-stag.yml
grep -Fq 'beavernest-app:lint' .github/workflows/beavernest-app-test-local-deploy-stag.yml
! test -e .github/workflows/beavernest-app-test-stag.yml
assert_no_match grep -Eq 'beavernest-app-web|Vercel preview|localhost:19320' .github/workflows/beavernest-app-test-local-deploy-stag.yml
