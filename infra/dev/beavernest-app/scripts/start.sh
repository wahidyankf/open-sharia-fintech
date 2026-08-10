#!/usr/bin/env bash
# Sole production entrypoint: explicit env file, then preflight, then one Compose service.
set -euo pipefail

beavernest_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd -P)

[[ $# -eq 2 && "$1" == --env-file ]] || {
	printf '%s\n' 'usage: start.sh --env-file PATH' >&2
	exit 1
}
beavernest_env_file=$2
[[ -f "$beavernest_env_file" && ! -L "$beavernest_env_file" ]] || {
	printf '%s\n' 'environment file must be a regular non-symlink file' >&2
	exit 1
}

beavernest_env_value() {
	awk -F= -v beavernest_key="$1" '$1 == beavernest_key { print substr($0, length(beavernest_key) + 2); exit }' "$beavernest_env_file"
}

BEAVERNEST_BE_VPN_HOST_IP=$(beavernest_env_value BEAVERNEST_BE_VPN_HOST_IP)
BEAVERNEST_BE_PUBLIC_PORT=$(beavernest_env_value BEAVERNEST_BE_PUBLIC_PORT)
BEAVERNEST_BE_HOST_DATA_DIRECTORY=$(beavernest_env_value BEAVERNEST_BE_HOST_DATA_DIRECTORY)
BEAVERNEST_BE_BACKUP_DIRECTORY=$(beavernest_env_value BEAVERNEST_BE_BACKUP_DIRECTORY)
export BEAVERNEST_BE_VPN_HOST_IP BEAVERNEST_BE_PUBLIC_PORT
export BEAVERNEST_BE_HOST_DATA_DIRECTORY BEAVERNEST_BE_BACKUP_DIRECTORY
bash "$beavernest_root/infra/dev/beavernest-app/scripts/preflight.sh"

exec docker compose --env-file "$beavernest_env_file" \
	-f "$beavernest_root/infra/dev/beavernest-app/docker-compose.yml" \
	up -d --build beavernest-app
