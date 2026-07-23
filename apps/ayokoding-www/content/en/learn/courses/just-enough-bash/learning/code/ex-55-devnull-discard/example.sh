#!/usr/bin/env bash
# Example 55: discarding output to /dev/null
set -euo pipefail

noisy_cmd() {             # => a function that prints to both streams, then fails on purpose
  echo "stdout noise"     # => an ordinary stdout line
  echo "stderr noise" >&2 # => an ordinary stderr line
  return 3                # => a non-zero exit status to prove it survives the redirection below
}                         # => closes the function

if noisy_cmd >/dev/null 2>&1; then # => `if` guards the call so set -e does not abort on the non-zero return
  status=0                         # => not reached in this run, since noisy_cmd always returns 3
else                               # => runs because noisy_cmd returned non-zero
  status=$?                        # => captures the real exit status (3) inside the else branch
fi                                 # => closes the if/else; no stdout/stderr from noisy_cmd was printed

echo "exit status: $status" # => proves the exit status survived even though all output was discarded
# => Output: exit status: 3 -- no "stdout noise" or "stderr noise" ever appears
