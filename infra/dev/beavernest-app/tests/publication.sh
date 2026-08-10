#!/usr/bin/env bash
set -euo pipefail

beavernest_compose=infra/dev/beavernest-app/docker-compose.yml
rg -Fq '${BEAVERNEST_BE_VPN_HOST_IP:-127.0.0.1}:${BEAVERNEST_BE_PUBLIC_PORT:-19300}:19300' "$beavernest_compose"
! rg -q '0\.0\.0\.0:|:19310:|:19320:' "$beavernest_compose"
[[ $(rg -c 'target: /var/lib/beavernest' "$beavernest_compose") -eq 4 ]]
