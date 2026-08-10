#!/usr/bin/env bash

set -euo pipefail

beavernest_development_directory=${BEAVERNEST_BE_DEVELOPMENT_DATA_DIRECTORY:-}

if [[ -z "$beavernest_development_directory" || ! -d "$beavernest_development_directory" || -L "$beavernest_development_directory" ]]; then
	echo "BEAVERNEST_BE_DEVELOPMENT_DATA_DIRECTORY must name an existing, non-symlink directory" >&2
	exit 1
fi

beavernest_canonical_directory=$(cd "$beavernest_development_directory" && pwd -P)
beavernest_repository_root=$(git rev-parse --show-toplevel)

case "$beavernest_canonical_directory" in
/ | "$HOME" | "$beavernest_repository_root" | "$beavernest_repository_root"/*)
	echo "development data directory must be outside the repository, root, and home directory" >&2
	exit 1
	;;
esac

unset BEAVERNEST_BE_HOST_DATA_DIRECTORY
unset BEAVERNEST_BE_VPN_HOST_IP
unset BEAVERNEST_BE_PUBLIC_PORT
unset BEAVERNEST_BE_BACKUP_DIRECTORY

export BEAVERNEST_BE_DATA_DIRECTORY="$beavernest_canonical_directory"
export BEAVERNEST_BE_HTTP_LISTEN_ADDRESS=127.0.0.1
export BEAVERNEST_BE_HTTP_LISTEN_PORT=19320

exec dotnet watch run --project apps/beavernest-be/src/BeaverNestBe/BeaverNestBe.fsproj
