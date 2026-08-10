#!/usr/bin/env bash
# Validate explicit production inputs before Docker Compose can render or start.
set -euo pipefail

beavernest_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd -P)
# shellcheck source=infra/dev/beavernest-app/scripts/lib.sh
source "$beavernest_root/infra/dev/beavernest-app/scripts/lib.sh"

: "${BEAVERNEST_BE_VPN_HOST_IP:?BEAVERNEST_BE_VPN_HOST_IP is required}"
: "${BEAVERNEST_BE_HOST_DATA_DIRECTORY:?BEAVERNEST_BE_HOST_DATA_DIRECTORY is required}"
: "${BEAVERNEST_BE_BACKUP_DIRECTORY:?BEAVERNEST_BE_BACKUP_DIRECTORY is required}"

beavernest_data_directory=$(beavernest_validate_safe_directory \
	'BEAVERNEST_BE_HOST_DATA_DIRECTORY' "$BEAVERNEST_BE_HOST_DATA_DIRECTORY" "$beavernest_root")
beavernest_backup_directory=$(beavernest_validate_safe_directory \
	'BEAVERNEST_BE_BACKUP_DIRECTORY' "$BEAVERNEST_BE_BACKUP_DIRECTORY" "$beavernest_root")
[[ "$beavernest_data_directory" != "$beavernest_backup_directory" ]] ||
	beavernest_fail 'data and backup directories must be distinct'
beavernest_validate_directory_mode 'BEAVERNEST_BE_HOST_DATA_DIRECTORY' "$beavernest_data_directory"
beavernest_validate_directory_mode 'BEAVERNEST_BE_BACKUP_DIRECTORY' "$beavernest_backup_directory"

if [[ "$BEAVERNEST_BE_VPN_HOST_IP" == 127.0.0.1 ]]; then
	[[ "${BEAVERNEST_BE_ALLOW_LOOPBACK_CI:-}" == 1 ]] ||
		beavernest_fail 'loopback publication is limited to explicit CI fixtures'
elif ! { command -v ip >/dev/null && ip -o addr show | awk '{print $4}' | cut -d/ -f1 | grep -Fxq "$BEAVERNEST_BE_VPN_HOST_IP"; } &&
	! { command -v ifconfig >/dev/null && ifconfig | awk '/inet / {print $2}' | grep -Fxq "$BEAVERNEST_BE_VPN_HOST_IP"; }; then
	beavernest_fail 'BEAVERNEST_BE_VPN_HOST_IP is not configured on this host'
fi
