#!/usr/bin/env bash
# Run golangci-lint over a gate-supplied list of changed Go files.
#
# The gate runner hands this wrapper a flat list of *.go paths relative to the
# repository root. golangci-lint cannot consume that list directly, for two
# reasons verified against 2.11.3:
#
#   1. A file list spanning more than one directory fails with
#      "named files must all be in one directory" (exit 7).
#   2. It resolves the Go module from its working directory, so invoking it from
#      the repository root — which holds no go.mod — fails with
#      "no go files to analyze" (exit 5).
#
# So map each path to its owning module and package directory, then run
# golangci-lint once per module from that module's root, passing the affected
# package directories. --path-prefix restores repository-relative paths in the
# output so a reader can click straight to the finding.
set -euo pipefail

if [ "$#" -eq 0 ]; then
	exit 0
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pairs="$(mktemp)"
trap 'rm -f "$pairs"' EXIT

for file; do
	# A deleted path still appears in the change set; it has nothing to lint.
	[ -e "$repo_root/$file" ] || continue

	dir="$(cd "$repo_root/$(dirname "$file")" && pwd)"
	module=""
	probe="$dir"
	while [ "$probe" != "/" ]; do
		if [ -f "$probe/go.mod" ]; then
			module="$probe"
			break
		fi
		probe="$(dirname "$probe")"
	done

	if [ -z "$module" ]; then
		printf '%s\n' "lint-golangci: no go.mod found above $file" >&2
		exit 1
	fi

	printf '%s\t%s\n' "$module" "${dir#"$module"/}" >>"$pairs"
done

[ -s "$pairs" ] || exit 0

status=0
while IFS= read -r module; do
	packages="$(awk -F'\t' -v m="$module" '$1 == m { print $2 }' "$pairs" | sort -u)"
	prefix="${module#"$repo_root"/}"

	# Drop directories whose Go files are all excluded by build constraints (a
	# `//go:build tools` pin, a platform-specific file). golangci-lint treats
	# such a directory as a typechecking error -- "build constraints exclude all
	# Go files" -- and fails the whole gate, even though nothing is wrong with
	# the code. `go list -e` reports them with zero GoFiles instead of erroring.
	buildable=""
	for pkg in $packages; do
		count="$(cd "$module" && go list -e -f '{{len .GoFiles}}{{len .TestGoFiles}}' "./$pkg" 2>/dev/null || echo "00")"
		[ "$count" = "00" ] && continue
		buildable="${buildable}${pkg}"$'\n'
	done
	packages="$(printf '%s' "$buildable")"
	[ -n "$packages" ] || continue

	# shellcheck disable=SC2086
	# $packages is a newline-separated list of module-relative directories that
	# must reach golangci-lint as separate arguments; none can contain a space,
	# because Go import paths cannot.
	(cd "$module" && golangci-lint run --path-prefix "$prefix" $packages) || status=1
done < <(cut -f1 "$pairs" | sort -u)

exit "$status"
