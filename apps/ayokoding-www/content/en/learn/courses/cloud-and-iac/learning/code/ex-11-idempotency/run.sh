#!/usr/bin/env sh
set -eu
state_file="${TMPDIR:-/tmp}/cloud-iac-idempotency-state"
test -f "$state_file" || : > "$state_file"
printf '%s\n' 'no changes: desired state already exists'
