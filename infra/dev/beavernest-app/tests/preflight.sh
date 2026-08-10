#!/usr/bin/env bash
# Contract tests for production preflight. Every fixture is task-owned.
set -euo pipefail

beavernest_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd -P)
beavernest_fixture=$(mktemp -d)
trap 'rm -rf -- "$beavernest_fixture"' EXIT

install -d -m 0700 "$beavernest_fixture/data" "$beavernest_fixture/backups"

run_preflight() {
	env -i \
		PATH="$PATH" \
		HOME="$HOME" \
		BEAVERNEST_BE_VPN_HOST_IP=127.0.0.1 \
		BEAVERNEST_BE_ALLOW_LOOPBACK_CI=1 \
		BEAVERNEST_BE_PUBLIC_PORT=19300 \
		BEAVERNEST_BE_HOST_DATA_DIRECTORY="$beavernest_fixture/data" \
		BEAVERNEST_BE_BACKUP_DIRECTORY="$beavernest_fixture/backups" \
		bash "$beavernest_root/infra/dev/beavernest-app/scripts/preflight.sh"
}

run_preflight

if env -i PATH="$PATH" HOME="$HOME" \
	BEAVERNEST_BE_ALLOW_LOOPBACK_CI=1 \
	BEAVERNEST_BE_HOST_DATA_DIRECTORY="$beavernest_fixture/data" \
	BEAVERNEST_BE_BACKUP_DIRECTORY="$beavernest_fixture/backups" \
	bash "$beavernest_root/infra/dev/beavernest-app/scripts/preflight.sh" >/dev/null 2>&1; then
	printf '%s\n' 'FAIL: absent host address passed preflight' >&2
	exit 1
fi

chmod 0755 "$beavernest_fixture/data"
if run_preflight >/dev/null 2>&1; then
	printf '%s\n' 'FAIL: unsafe data-directory mode passed preflight' >&2
	exit 1
fi
chmod 0700 "$beavernest_fixture/data"

ln -s "$beavernest_fixture/data" "$beavernest_fixture/data-alias"
if env -i PATH="$PATH" HOME="$HOME" BEAVERNEST_BE_VPN_HOST_IP=127.0.0.1 \
	BEAVERNEST_BE_ALLOW_LOOPBACK_CI=1 BEAVERNEST_BE_HOST_DATA_DIRECTORY="$beavernest_fixture/data-alias" \
	BEAVERNEST_BE_BACKUP_DIRECTORY="$beavernest_fixture/backups" \
	bash "$beavernest_root/infra/dev/beavernest-app/scripts/preflight.sh" >/dev/null 2>&1; then
	printf '%s\n' 'FAIL: symlinked data directory passed preflight' >&2
	exit 1
fi

beavernest_repo_subdir="$beavernest_root/local-temp/beavernest-preflight-subdir-of-repo-$$"
install -d -m 0700 "$beavernest_repo_subdir"
trap 'rm -rf -- "$beavernest_fixture" "$beavernest_repo_subdir"' EXIT
if env -i PATH="$PATH" HOME="$HOME" BEAVERNEST_BE_VPN_HOST_IP=127.0.0.1 \
	BEAVERNEST_BE_ALLOW_LOOPBACK_CI=1 BEAVERNEST_BE_HOST_DATA_DIRECTORY="$beavernest_repo_subdir" \
	BEAVERNEST_BE_BACKUP_DIRECTORY="$beavernest_fixture/backups" \
	bash "$beavernest_root/infra/dev/beavernest-app/scripts/preflight.sh" >/dev/null 2>&1; then
	printf '%s\n' 'FAIL: data directory nested inside the git repository passed preflight' >&2
	exit 1
fi
