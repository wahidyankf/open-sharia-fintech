#!/usr/bin/env bash
# Regression: CI provides API_BASE_URL after it starts the full stack, so the
# backend E2E wrapper must not start another Compose project on the same port.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
TEMP_DIRECTORY="$(mktemp -d)"
MOCK_BIN="${TEMP_DIRECTORY}/bin"
DOCKER_LOG="${TEMP_DIRECTORY}/docker-called"

cleanup() {
	rm -rf "${TEMP_DIRECTORY}"
}
trap cleanup EXIT

mkdir -p "${MOCK_BIN}"
printf '#!/usr/bin/env bash\ntouch "${DOCKER_LOG:?}"\nexit 97\n' >"${MOCK_BIN}/docker"
printf '#!/usr/bin/env bash\nexit 0\n' >"${MOCK_BIN}/curl"
printf '#!/usr/bin/env bash\nexit 0\n' >"${MOCK_BIN}/npx"
chmod +x "${MOCK_BIN}/docker" "${MOCK_BIN}/curl" "${MOCK_BIN}/npx"

DOCKER_LOG="${DOCKER_LOG}" API_BASE_URL="http://127.0.0.1:19320" PATH="${MOCK_BIN}:${PATH}" \
	bash "${ROOT}/apps/beavernest-be/scripts/run-e2e.sh"

test ! -e "${DOCKER_LOG}"
