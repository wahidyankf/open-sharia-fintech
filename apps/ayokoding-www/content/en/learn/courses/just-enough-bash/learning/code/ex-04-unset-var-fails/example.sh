#!/usr/bin/env bash
# Example 4: Unset Var Fails
set -u # => enables "nounset": referencing an undefined variable is now an error
# shellcheck disable=SC2154 # => intentional: this line demonstrates set -u catching a real unset variable
echo "${undefined_var}" # => undefined_var was never assigned, so this line aborts the script
# => stderr: example.sh: line 5: undefined_var: unbound variable
