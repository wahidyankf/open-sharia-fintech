#!/usr/bin/env bash
# Verify every actions/upload-artifact step declares an explicit retention-days.
#
# An upload step with no retention-days inherits the repository default, which
# GitHub ships at 90 days. A per-run scratch artifact retained for 90 days
# multiplies by the run rate and silently consumes the account-wide Actions
# storage quota, so the retention window is a required, reviewable declaration
# rather than an inherited default.
set -euo pipefail

list="$(mktemp)"
trap 'rm -f "$list"' EXIT

if [ "$#" -eq 0 ]; then
	find .github/workflows -maxdepth 1 -type f \
		\( -name '*.yml' -o -name '*.yaml' \) | sort >"$list"
else
	printf '%s\n' "$@" >"$list"
fi

status=0
while IFS= read -r file; do
	[ -n "$file" ] || continue
	[ -f "$file" ] || continue

	if ! awk -v FILE="$file" '
		{ line[NR] = $0 }
		END {
			nb = 0
			for (i = 1; i <= NR; i++) {
				s = line[i]
				if (s ~ /^[ \t]*#/) continue
				if (s !~ /^[ \t]*-([ \t]|$)/) continue
				nb++
				bullet[nb] = i
				pos = index(s, "-")
				indent[nb] = pos - 1
			}

			bad = 0
			for (i = 1; i <= NR; i++) {
				s = line[i]
				if (s ~ /^[ \t]*#/) continue
				if (s !~ /uses:[ \t]*[^ \t]*actions\/upload-artifact/) continue

				owner = 0
				for (b = 1; b <= nb; b++) {
					if (bullet[b] <= i) owner = b; else break
				}
				if (owner == 0) { start = 1; stop = NR }
				else {
					start = bullet[owner]
					stop = NR
					for (c = owner + 1; c <= nb; c++) {
						if (indent[c] <= indent[owner]) { stop = bullet[c] - 1; break }
					}
				}

				found = 0
				for (j = start; j <= stop; j++) {
					t = line[j]
					if (t ~ /^[ \t]*#/) continue
					if (t ~ /retention-days[ \t]*:/) { found = 1; break }
				}
				if (!found) {
					printf "%s:%d: upload-artifact step has no retention-days\n", FILE, i > "/dev/stderr"
					bad = 1
				}
			}
			exit bad
		}
	' "$file"; then
		status=1
	fi
done <"$list"

if [ "$status" -ne 0 ]; then
	printf '%s\n' \
		"Every actions/upload-artifact step must declare retention-days." \
		"Without it the step inherits the repository default (90 days on a new repo)." >&2
fi

exit "$status"
