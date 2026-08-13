#!/usr/bin/env bash
# Own one disposable combined runtime, then invoke exactly one pure Playwright runner.
set -euo pipefail

beavernest_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd -P)

# Fail fast (before paying for docker-compose/dotnet startup) on any unconditional
# test.skip() left in either e2e suite this script can hand off to.
# test.skip(condition, reason) - the documented Playwright environment-guard form -
# is intentionally allowed through.
if grep -rn -E --include='*.ts' --exclude-dir=node_modules --exclude-dir=.features-gen --exclude-dir=test-results --exclude-dir=playwright-report '\$?test\.skip\([^,)]*\)' "${beavernest_root}/apps/beavernest-be-e2e" "${beavernest_root}/apps/beavernest-app-e2e"; then
	echo "ERROR: unconditional test.skip() found in test files above - use test.skip(condition, reason) for legitimate environment guards, or remove" >&2
	exit 1
fi

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
		WEB_BASE_URL="$beavernest_web_base_url" bash "$beavernest_root/apps/beavernest-app-e2e/scripts/run-playwright.sh"
	fi
	exit 0
fi

beavernest_fixture_root=$(mktemp -d)
beavernest_project="beavernest-e2e-${RANDOM}-${RANDOM}"
export APP_ENV="${APP_ENV:-test}"
beavernest_compose=(docker compose --env-file /dev/null -p "$beavernest_project"
	-f "$beavernest_root/infra/dev/beavernest-app/docker-compose.yml"
	-f "$beavernest_root/infra/dev/beavernest-app/docker-compose.ci.yml")

cleanup() {
	"${beavernest_compose[@]}" down --remove-orphans >/dev/null 2>&1 || true
	rm -rf -- "$beavernest_fixture_root"
}
trap cleanup EXIT

install -d -m 0700 "$beavernest_fixture_root/data" "$beavernest_fixture_root/backups"
# Randomized (not the fixed production default 19300) so a backend and a
# frontend disposable runtime — each its own `docker compose` project, each
# started by this same script — can run concurrently (e.g.
# `nx run-many -t test:e2e -p beavernest-be-e2e,beavernest-app-e2e`)
# without one's host port bind failing on the other's.
beavernest_public_port=$((20000 + (RANDOM % 10000)))
export BEAVERNEST_BE_VPN_HOST_IP=127.0.0.1
export BEAVERNEST_BE_PUBLIC_PORT=$beavernest_public_port
export BEAVERNEST_BE_HOST_DATA_DIRECTORY="$beavernest_fixture_root/data"
export BEAVERNEST_BE_BACKUP_DIRECTORY="$beavernest_fixture_root/backups"
beavernest_e2e_uid="$(id -u)"
beavernest_e2e_gid="$(id -g)"
export BEAVERNEST_BE_E2E_UID="$beavernest_e2e_uid"
export BEAVERNEST_BE_E2E_GID="$beavernest_e2e_gid"

# The beavernest-be-e2e Playwright suite talks deep SQLite internals directly
# on this machine's own dotnet SDK (never inside the SDK-less runtime
# container — see apps/beavernest-be-e2e/utils/host-runtime.ts) against these
# same host-bind-mounted files, and needs a fresh Debug build to `#r`.
dotnet build "$beavernest_root/apps/beavernest-be/src/BeaverNestBe/BeaverNestBe.fsproj" --nologo -v quiet
export BEAVERNEST_BE_E2E_DATA_DIRECTORY="$beavernest_fixture_root/data"
export BEAVERNEST_BE_E2E_BACKUP_DIRECTORY="$beavernest_fixture_root/backups"

"${beavernest_compose[@]}" build beavernest-app
"${beavernest_compose[@]}" up -d beavernest-app

beavernest_api_base_url="http://127.0.0.1:$beavernest_public_port"
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
	WEB_BASE_URL="$beavernest_api_base_url" bash "$beavernest_root/apps/beavernest-app-e2e/scripts/run-playwright.sh"
fi
