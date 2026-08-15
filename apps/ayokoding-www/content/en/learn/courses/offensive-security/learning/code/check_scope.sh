#!/usr/bin/env sh
# Authorized lab target only: this script reads a local fixture and never opens a network connection.
set -eu

fixture="${1:-$(dirname "$0")/lab-evidence.json}"

test -f "$fixture" || {
	echo "scope rejected: fixture is missing" >&2
	exit 1
}
grep -Fq '"authorization": "I OWN THIS LAB"' "$fixture" || {
	echo "scope rejected: owner authorization is missing" >&2
	exit 1
}
grep -Eq '"target": "(localhost|127\.0\.0\.1)"' "$fixture" || {
	echo "scope rejected: target must be localhost or 127.0.0.1" >&2
	exit 1
}

echo "scope accepted: authorized self-owned local lab fixture"
