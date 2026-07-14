#!/usr/bin/env bash
# Example 79: atomic write via mktemp + mv -- only publish on success
set -euo pipefail # => same strict-mode header as every other example in this primer

out="result.txt"             # => the final path -- callers must never see a half-written version of it
scratch="$(mktemp)"          # => a private scratch file, invisible to any reader of $out until the final mv
trap 'rm -f "$scratch"' EXIT # => cleans up scratch if anything below fails BEFORE the final mv
# => trap is registered immediately after scratch exists, so no failure window is left unguarded

mode="${1:-ok}" # => "ok" (the default) succeeds; "fail" simulates a mid-pipeline failure

echo "line one" >"$scratch"                # => first line of real output, written to scratch only, never touching $out
if [[ "$mode" == "fail" ]]; then           # => simulates a failure partway through building the output
  echo "example.sh: simulated failure" >&2 # => the error goes to stderr, the conventional channel
  exit 1                                   # => aborts BEFORE the mv below -- $out is never created here
fi                                         # => closes the if
echo "line two" >>"$scratch"               # => second line, reached only on the successful path

mv "$scratch" "$out" # => atomic: $out either has ALL the output at once, or none of it
echo "wrote: $out"   # => confirms the atomic publish succeeded
