#!/usr/bin/env bash
# Contract tests for production preflight. Every fixture is task-owned.
set -euo pipefail

beavernest_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd -P)
beavernest_fixture=$(mktemp -d)
trap 'rm -rf -- "$beavernest_fixture"' EXIT

install -d -m 0700 "$beavernest_fixture/data" "$beavernest_fixture/backups"

# GNU stat treats -f as filesystem reporting: it can print metadata before
# failing to parse BSD's %Lp directive. The helper must discard that output
# and use the GNU mode query instead.
beavernest_mock_bin="$beavernest_fixture/mock-bin"
install -d -m 0700 "$beavernest_mock_bin"
beavernest_mock_stat="$beavernest_mock_bin/stat"
cat >"$beavernest_mock_stat" <<'EOF'
#!/usr/bin/env bash
case "$1" in
-f)
	printf '%s\n' 'filesystem metadata that must not become a mode'
	exit 1
	;;
-c)
	printf '%s\n' 700
	;;
*)
	exit 1
	;;
esac
EOF
chmod 0700 "$beavernest_mock_stat"

# shellcheck source=infra/dev/beavernest-app/scripts/lib.sh
source "$beavernest_root/infra/dev/beavernest-app/scripts/lib.sh"
beavernest_original_path=$PATH
PATH="$beavernest_mock_bin:$PATH"
if ! beavernest_validate_directory_mode 'mock Linux directory' "$beavernest_fixture/data"; then
	printf '%s\n' 'FAIL: Linux stat fallback rejected mode 0700' >&2
	exit 1
fi
PATH=$beavernest_original_path

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

beavernest_repo_subdir="$beavernest_root/local-tmp/beavernest-preflight-subdir-of-repo-$$"
install -d -m 0700 "$beavernest_repo_subdir"
trap 'rm -rf -- "$beavernest_fixture" "$beavernest_repo_subdir"' EXIT
if env -i PATH="$PATH" HOME="$HOME" BEAVERNEST_BE_VPN_HOST_IP=127.0.0.1 \
	BEAVERNEST_BE_ALLOW_LOOPBACK_CI=1 BEAVERNEST_BE_HOST_DATA_DIRECTORY="$beavernest_repo_subdir" \
	BEAVERNEST_BE_BACKUP_DIRECTORY="$beavernest_fixture/backups" \
	bash "$beavernest_root/infra/dev/beavernest-app/scripts/preflight.sh" >/dev/null 2>&1; then
	printf '%s\n' 'FAIL: data directory nested inside the git repository passed preflight' >&2
	exit 1
fi

# Reverse containment direction: a data directory that is an *ancestor* of the
# repository root (e.g. a dev running the backend with cwd nested under $HOME)
# must be rejected too — beavernest_validate_safe_directory's second `case`
# arm (`"$beavernest_repository_root" in "$beavernest_canonical"/*)`).
# Skip the immediate parent if it happens to equal $HOME on this host, since
# that would exercise the (already-tested) home-equality arm instead of the
# ancestor arm this test targets.
beavernest_repo_ancestor=$(dirname -- "$beavernest_root")
beavernest_home_canonical=$(cd -P -- "$HOME" && pwd -P)
if [[ "$beavernest_repo_ancestor" == "$beavernest_home_canonical" ]]; then
	beavernest_repo_ancestor=$(dirname -- "$beavernest_repo_ancestor")
fi
if env -i PATH="$PATH" HOME="$HOME" BEAVERNEST_BE_VPN_HOST_IP=127.0.0.1 \
	BEAVERNEST_BE_ALLOW_LOOPBACK_CI=1 BEAVERNEST_BE_HOST_DATA_DIRECTORY="$beavernest_repo_ancestor" \
	BEAVERNEST_BE_BACKUP_DIRECTORY="$beavernest_fixture/backups" \
	bash "$beavernest_root/infra/dev/beavernest-app/scripts/preflight.sh" >/dev/null 2>&1; then
	printf '%s\n' 'FAIL: data directory that is an ancestor of the git repository passed preflight' >&2
	exit 1
fi
