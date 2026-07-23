#!/usr/bin/env bash
# Example 80: trap ... ERR reports the line where a command failed
set -euo pipefail

trap 'echo "failed at line $LINENO" >&2' ERR
# => ERR fires whenever a command's exit status is non-zero, in the same places set -e would abort
# => $LINENO inside the trap resolves to the line number of the command that just failed
echo "starting"      # => runs normally, before the failure below
false                # => this command's exit status is 1; that is what triggers the ERR trap above
echo "never reached" # => set -e means the script aborts right after the trap fires, before this line
