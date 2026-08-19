#!/usr/bin/env bash
# E2E test runner for organiclever-be.
# Brings up PostgreSQL + NATS via docker-compose, starts the F# backend on
# port 8202, runs the organiclever-be-e2e Playwright suite against it, then tears down.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

# Fail fast (before paying for docker-compose/dotnet startup) on any unconditional
# test.skip() left in the e2e suite. test.skip(condition, reason) - the documented
# Playwright environment-guard form - is intentionally allowed through.
if grep -rn -E --include='*.ts' --exclude-dir=node_modules --exclude-dir=.features-gen --exclude-dir=test-results --exclude-dir=playwright-report '\$?test\.skip\([^,)]*\)' "${ROOT}/apps/organiclever-be-e2e"; then
	echo "ERROR: unconditional test.skip() found in test files above - use test.skip(condition, reason) for legitimate environment guards, or remove" >&2
	exit 1
fi

COMPOSE_FILE="${ROOT}/apps/organiclever-be/docker-compose.e2e.yml"
PROJECT_NAME="organiclever-be-e2e"
PORT=8202
FSPROJ="${ROOT}/apps/organiclever-be/src/OrganicleverBe/OrganicleverBe.fsproj"
BE_PID=""

cleanup() {
	if [[ -n "${BE_PID}" ]]; then
		kill "${BE_PID}" 2>/dev/null || true
		wait "${BE_PID}" 2>/dev/null || true
	fi
	docker compose -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" down -v >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Start infrastructure
docker compose -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" down -v >/dev/null 2>&1 || true
docker compose -p "${PROJECT_NAME}" -f "${COMPOSE_FILE}" up -d --wait

# Build the backend
dotnet build "${FSPROJ}" --configuration Release --nologo -v quiet

# Start backend in background
export DATABASE_URL="Host=localhost;Port=5436;Database=organiclever;Username=postgres;Password=postgres"
export ORGANICLEVER_BE_PORT="${PORT}"
export ORGANICLEVER_BE_CORS_ORIGINS="*"
export ORGANICLEVER_BE_NATS_URL="nats://localhost:4226"

dotnet run --project "${FSPROJ}" --no-build --configuration Release &
BE_PID="$!"

# Wait until the health endpoint responds (up to 60 s)
echo "Waiting for organiclever-be on port ${PORT}..."
for i in $(seq 1 60); do
	if curl -sf "http://localhost:${PORT}/api/v1/health" >/dev/null 2>&1; then
		echo "organiclever-be is ready (${i}s)"
		break
	fi
	if [[ "${i}" -eq 60 ]]; then
		echo "ERROR: organiclever-be did not start within 60 seconds" >&2
		exit 1
	fi
	sleep 1
done

# Run the Playwright e2e suite
cd "${ROOT}/apps/organiclever-be-e2e"
npx bddgen && npx playwright test
