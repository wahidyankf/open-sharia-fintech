#!/usr/bin/env bash
# Own one disposable combined runtime, then invoke exactly one pure Playwright runner.
set -euo pipefail

beavernest_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd -P)
beavernest_suite=backend
if [[ "${1:-}" == --frontend ]]; then
	beavernest_suite=frontend
	shift
fi
[[ $# -eq 0 ]] || {
	printf '%s\n' 'usage: run-e2e.sh [--frontend]' >&2
	exit 1
}

beavernest_api_base_url=${API_BASE_URL:-}
beavernest_web_base_url=${WEB_BASE_URL:-}
if [[ -n "$beavernest_api_base_url$beavernest_web_base_url" ]]; then
	if [[ "$beavernest_suite" == backend ]]; then
		[[ -n "$beavernest_api_base_url" ]] || {
			printf '%s\n' 'API_BASE_URL is required for an existing runtime' >&2
			exit 1
		}
		API_BASE_URL="$beavernest_api_base_url" bash "$beavernest_root/apps/beavernest-be-e2e/scripts/run-playwright.sh"
	else
		[[ -n "$beavernest_web_base_url" ]] || {
			printf '%s\n' 'WEB_BASE_URL is required for an existing runtime' >&2
			exit 1
		}
		WEB_BASE_URL="$beavernest_web_base_url" bash "$beavernest_root/apps/beavernest-app-web-e2e/scripts/run-playwright.sh"
	fi
	exit 0
fi

beavernest_fixture_root=$(mktemp -d)
beavernest_project="beavernest-e2e-${RANDOM}-${RANDOM}"
beavernest_compose=(docker compose --env-file /dev/null -p "$beavernest_project"
	-f "$beavernest_root/infra/dev/beavernest-app/docker-compose.yml"
	-f "$beavernest_root/infra/dev/beavernest-app/docker-compose.ci.yml")

cleanup() {
	"${beavernest_compose[@]}" down --remove-orphans >/dev/null 2>&1 || true
	rm -rf -- "$beavernest_fixture_root"
}
trap cleanup EXIT

install -d -m 0700 "$beavernest_fixture_root/data" "$beavernest_fixture_root/backups"
export BEAVERNEST_BE_VPN_HOST_IP=127.0.0.1
export BEAVERNEST_BE_PUBLIC_PORT=19300
export BEAVERNEST_BE_HOST_DATA_DIRECTORY="$beavernest_fixture_root/data"
export BEAVERNEST_BE_BACKUP_DIRECTORY="$beavernest_fixture_root/backups"

"${beavernest_compose[@]}" build beavernest-app
"${beavernest_compose[@]}" run --rm --no-deps --user 0:0 --entrypoint sh beavernest-app -ceu \
	'chown 10001:10001 /var/lib/beavernest && chmod 0700 /var/lib/beavernest'
"${beavernest_compose[@]}" up -d beavernest-app

beavernest_api_base_url=http://127.0.0.1:19300
for beavernest_attempt in $(seq 1 120); do
	if curl -fsS "$beavernest_api_base_url/api/v1/readiness" >/dev/null 2>&1; then
		break
	fi
	[[ "$beavernest_attempt" -lt 120 ]] || {
		printf '%s\n' 'combined runtime did not become ready' >&2
		exit 1
	}
	sleep 1
done

if [[ "$beavernest_suite" == backend ]]; then
	API_BASE_URL="$beavernest_api_base_url" \
		BEAVERNEST_BE_E2E_COMPOSE_PROJECT="$beavernest_project" \
		bash "$beavernest_root/apps/beavernest-be-e2e/scripts/run-playwright.sh"
else
	WEB_BASE_URL="$beavernest_api_base_url" bash "$beavernest_root/apps/beavernest-app-web-e2e/scripts/run-playwright.sh"
fi
