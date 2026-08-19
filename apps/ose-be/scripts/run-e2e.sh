#!/usr/bin/env bash
# E2E test runner for ose-be.
# Brings up PostgreSQL + NATS via docker-compose, starts the F# backend on
# port 8302, runs the ose-be-e2e Playwright suite against it, then tears down.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

# Fail fast (before paying for docker-compose/dotnet startup) on any unconditional
# test.skip() left in the e2e suite. test.skip(condition, reason) - the documented
# Playwright environment-guard form - is intentionally allowed through.
if grep -rn -E --include='*.ts' --exclude-dir=node_modules --exclude-dir=.features-gen --exclude-dir=test-results --exclude-dir=playwright-report '\$?test\.skip\([^,)]*\)' "${ROOT}/apps/ose-be-e2e"; then
	echo "ERROR: unconditional test.skip() found in test files above - use test.skip(condition, reason) for legitimate environment guards, or remove" >&2
	exit 1
fi

COMPOSE_FILE="${ROOT}/apps/ose-be/docker-compose.e2e.yml"
PROJECT_NAME="ose-be-e2e"
PORT=8302
FSPROJ="${ROOT}/apps/ose-be/src/OseBe/OseBe.fsproj"
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
export DATABASE_URL="Host=localhost;Port=5435;Database=ose_app;Username=postgres;Password=postgres"
export OSE_BE_PORT="${PORT}"
export OSE_BE_CORS_ORIGINS="*"
export OSE_BE_NATS_URL="nats://localhost:4225"
export OSE_BE_OPENROUTER_API_KEY=""
export OSE_BE_OPENROUTER_MODEL="openrouter/auto"
export OSE_BE_OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"

dotnet run --project "${FSPROJ}" --no-build --configuration Release &
BE_PID="$!"

# Wait until the health endpoint responds (up to 60 s)
echo "Waiting for ose-be on port ${PORT}..."
for i in $(seq 1 60); do
	if curl -sf "http://localhost:${PORT}/api/v1/health" >/dev/null 2>&1; then
		echo "ose-be is ready (${i}s)"
		break
	fi
	if [[ "${i}" -eq 60 ]]; then
		echo "ERROR: ose-be did not start within 60 seconds" >&2
		exit 1
	fi
	sleep 1
done

# Run the Playwright e2e suite
cd "${ROOT}/apps/ose-be-e2e"
npx bddgen && npx playwright test
