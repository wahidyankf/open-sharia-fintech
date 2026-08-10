#!/usr/bin/env bash

# Verifies that the production entrypoint rejects unsafe persistent-storage
# ownership and modes before handing control to the application process.
set -euo pipefail

beavernest_repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
beavernest_entrypoint="$beavernest_repository_root/apps/beavernest-be/scripts/container-entrypoint.sh"
beavernest_test_image="beavernest-container-permissions:local"

if [[ ! -f "$beavernest_entrypoint" ]]; then
	printf 'FAIL: expected container entrypoint at %s\n' "$beavernest_entrypoint" >&2
	exit 1
fi

cleanup() {
	docker image rm --force "$beavernest_test_image" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker build --tag "$beavernest_test_image" --file - "$beavernest_repository_root" <<'DOCKERFILE'
FROM mcr.microsoft.com/dotnet/sdk:10.0.302-noble@sha256:72dd743782f2ae7e5476fd64f6a460045e3998dc862218b80e6944cba79a01b0

RUN groupadd --gid 10001 beavernest \
  && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin beavernest \
  && install --directory --owner=10001 --group=10001 --mode=0700 /fixtures/safe /fixtures/unsafe-mode /fixtures/unsafe-file-mode \
  && install --directory --owner=0 --group=0 --mode=0700 /fixtures/unsafe-owner \
  && install --owner=10001 --group=10001 --mode=0600 /dev/null /fixtures/safe/beavernest.db \
  && install --owner=10001 --group=10001 --mode=0600 /dev/null /fixtures/safe/beavernest.db-wal \
  && install --owner=10001 --group=10001 --mode=0600 /dev/null /fixtures/safe/beavernest.db-shm \
  && install --owner=10001 --group=10001 --mode=0600 /dev/null /fixtures/safe/backup.sqlite \
  && install --owner=10001 --group=10001 --mode=0644 /dev/null /fixtures/unsafe-file-mode/beavernest.db \
  && chmod 0755 /fixtures/unsafe-mode

COPY apps/beavernest-be/scripts/container-entrypoint.sh /app/container-entrypoint.sh
RUN chmod 0755 /app/container-entrypoint.sh

USER 10001:10001
ENTRYPOINT ["/app/container-entrypoint.sh"]
DOCKERFILE

docker run --rm \
	--env BEAVERNEST_BE_DATA_DIRECTORY=/fixtures/safe \
	"$beavernest_test_image" \
	sh -c 'test "$(umask)" = "0077"'

if docker run --rm \
	--env BEAVERNEST_BE_DATA_DIRECTORY=/fixtures/unsafe-owner \
	"$beavernest_test_image" \
	true; then
	printf '%s\n' 'FAIL: unsafe persistent-storage ownership was accepted' >&2
	exit 1
fi

if docker run --rm \
	--env BEAVERNEST_BE_DATA_DIRECTORY=/fixtures/unsafe-mode \
	"$beavernest_test_image" \
	true; then
	printf '%s\n' 'FAIL: unsafe persistent-storage mode was accepted' >&2
	exit 1
fi

if docker run --rm \
	--env BEAVERNEST_BE_DATA_DIRECTORY=/fixtures/unsafe-file-mode \
	"$beavernest_test_image" \
	true; then
	printf '%s\n' 'FAIL: unsafe SQLite-file mode was accepted' >&2
	exit 1
fi

printf '%s\n' 'PASS: container persistent-storage permissions are fail-closed'
