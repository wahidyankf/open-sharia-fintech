#!/usr/bin/env bash
# Run one guarded database operation using an explicitly supplied environment file.
set -euo pipefail

beavernest_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd -P)
# shellcheck source=infra/dev/beavernest-app/scripts/lib.sh
source "$beavernest_root/infra/dev/beavernest-app/scripts/lib.sh"

[[ $# -ge 3 ]] || beavernest_fail 'usage: operations.sh {backup|integrity|restore} --env-file PATH [--name NAME.sqlite3]'
beavernest_operation=$1
[[ "$2" == --env-file ]] || beavernest_fail 'the explicit --env-file argument is required'
beavernest_env_file=$3
shift 3
[[ -f "$beavernest_env_file" && ! -L "$beavernest_env_file" ]] || beavernest_fail 'environment file must be a regular non-symlink file'

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

case "$beavernest_operation" in
backup | restore)
	[[ $# -eq 2 && "$1" == --name ]] || beavernest_fail 'backup and restore require --name NAME.sqlite3'
	beavernest_validate_operation_name "$2"
	export BEAVERNEST_BE_OPERATION_NAME=$2
	;;
integrity) [[ $# -eq 0 ]] || beavernest_fail 'integrity does not accept a name' ;;
*) beavernest_fail 'operation must be backup, integrity, or restore' ;;
esac

beavernest_compose=(docker compose --env-file "$beavernest_env_file" -f "$beavernest_root/infra/dev/beavernest-app/docker-compose.yml")
if [[ "$beavernest_operation" == restore ]] && "${beavernest_compose[@]}" ps --services --status running | grep -Fxq beavernest-app; then
	beavernest_fail 'restore refused while beavernest-app is running'
fi

case "$beavernest_operation" in
backup) "${beavernest_compose[@]}" run --rm beavernest-backup ;;
integrity) "${beavernest_compose[@]}" run --rm beavernest-integrity ;;
restore) "${beavernest_compose[@]}" run --rm beavernest-restore ;;
esac
