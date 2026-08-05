#!/usr/bin/env bash
# Verify Go formatting without modifying any source file.
# `gofmt -l` prints each unformatted path but still exits zero, so its output
# must be converted into this verifier's non-zero result.
set -euo pipefail

if [ "$#" -eq 0 ]; then
	exit 0
fi

if ! unformatted="$(gofmt -l "$@")"; then
	exit 1
fi

if [ -n "$unformatted" ]; then
	printf '%s\n' "Go files need formatting:" >&2
	printf '%s\n' "$unformatted" >&2
	exit 1
fi
