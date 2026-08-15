#!/usr/bin/env sh
# => Runs entirely locally and checks that this teaching skeleton contains required non-secret placeholders.
set -eu
# => Resolves the course root from this script without depending on the caller's working directory.
course_root=$(CDPATH='' cd -- "$(dirname -- "$0")/../.." && pwd)
# => Fails if a token-shaped assignment accidentally enters a reviewed teaching artifact.
if rg -n 'api_token\s*=\s*"[^$][^"]+"|BEGIN (RSA|OPENSSH) PRIVATE KEY' "$course_root/learning/capstone"; then
	printf '%s\n' 'unsafe secret-shaped value found' >&2
	exit 1
fi
# => Requires the deliberate external-secret and recovery placeholders before a reader copies the skeleton.
rg -q 'variable "proxmox_api_token"' "$course_root/learning/capstone/terraform/variables.tf"
rg -q 'RESTORE EVIDENCE' "$course_root/learning/capstone/recovery-drill.md"
# => Reports a local validation result; no provider, guest, disk, or network request was used.
printf '%s\n' 'bare-metal virtualization skeleton: local validation passed'
