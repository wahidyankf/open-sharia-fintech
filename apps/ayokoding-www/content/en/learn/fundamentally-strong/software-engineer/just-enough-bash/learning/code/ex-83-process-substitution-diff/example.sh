#!/usr/bin/env bash
# Example 83: process substitution -- diffing two live pipelines, no temp files needed
set -euo pipefail

diff <(sort a.txt) <(sort b.txt) >psub.diff || true
# => <(cmd) runs cmd in a subshell and exposes its stdout as a file-like path diff can read directly
# => diff exits non-zero when its inputs differ; || true lets this script keep running past that
# => Output (redirected to psub.diff): the unified-style diff of the two SORTED files

scratch_a="$(mktemp)" # => stages the same sorted content the traditional way, for a comparison only
scratch_b="$(mktemp)" # => a second staging file, also sorted the traditional way
trap 'rm -f "$scratch_a" "$scratch_b"' EXIT
sort a.txt >"$scratch_a" # => identical sort to the one inside the process substitution above
sort b.txt >"$scratch_b" # => identical sort to the one inside the process substitution above
diff "$scratch_a" "$scratch_b" >staged.diff || true
# => the traditional temp-file-staged equivalent of the process-substitution diff above

diff psub.diff staged.diff && echo "process substitution matches temp-file staging"
# => Output: process substitution matches temp-file staging

diff <(sort a.txt) <(sort a.txt) >/dev/null && echo "no differences for identical input"
# => sorting the SAME file against itself always produces an empty diff
# => Output: no differences for identical input
