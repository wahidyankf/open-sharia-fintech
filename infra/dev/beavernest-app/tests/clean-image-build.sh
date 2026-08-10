#!/usr/bin/env bash

# Build the production image from a source-only copy. This prevents an image
# build from accidentally consuming generated clients or frontend output left
# in a developer's working tree.
set -euo pipefail

beavernest_repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
beavernest_build_root="$(mktemp -d)"
beavernest_image="beavernest-app:clean-image-build"

cleanup() {
	rm -rf -- "$beavernest_build_root"
	docker image rm --force "$beavernest_image" >/dev/null 2>&1 || true
}
trap cleanup EXIT

rsync --archive --delete \
	--exclude='.git/' \
	--exclude='node_modules/' \
	--exclude='.nx/' \
	--exclude='dist/' \
	--exclude='.next/' \
	--exclude='coverage/' \
	--exclude='generated-reports/' \
	--exclude='apps/beavernest-app-web/src/generated-contracts/' \
	--exclude='specs/apps/beavernest/containers/contracts/generated/' \
	"$beavernest_repository_root/" \
	"$beavernest_build_root/"

docker build \
	--file "$beavernest_build_root/apps/beavernest-be/Dockerfile" \
	--tag "$beavernest_image" \
	"$beavernest_build_root"

docker run --rm --entrypoint sh "$beavernest_image" \
	-c 'test ! -x /usr/bin/node && test "$(id -u):$(id -g)" = "10001:10001"'

printf '%s\n' 'PASS: production image builds from source-only inputs as 10001:10001'
