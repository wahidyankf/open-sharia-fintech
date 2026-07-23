#!/usr/bin/env bash
# Example 57: usage text and errors with getopts
set -euo pipefail

usage() {                            # => prints one-line usage text, shared by every caller that needs it
  echo "usage: example.sh [-h] [-v]" # => the text itself
}                                    # => closes usage

parse() {                                 # => parses one simulated set of flags, passed in as "$@"
  local OPTIND=1 opt                      # => local OPTIND resets getopts state on every call to parse
  while getopts ":hv" opt "$@"; do        # => leading : enables SILENT error handling (no built-in message)
    case "$opt" in                        # => $opt holds the parsed option letter, or ? on an invalid one
    h)                                    # => matches when -h was passed
      usage                               # => prints the shared usage text
      return 0                            # => -h exits successfully (status 0)
      ;;                                  # => ends this branch
    v)                                    # => matches when -v was passed
      echo "verbose mode"                 # => confirms verbose mode was recognized
      ;;                                  # => ends this branch
    \?)                                   # => matches any option NOT in ":hv" (an invalid flag)
      echo "invalid option: -$OPTARG" >&2 # => $OPTARG holds the invalid letter; reported on stderr
      return 1                            # => an invalid option exits with a non-zero status
      ;;                                  # => ends this branch
    esac                                  # => closes the case statement
  done                                    # => closes the while-loop
  return 0                                # => reached only if every flag parsed cleanly with no -h
}                                         # => closes parse

# two probes: a valid -h flag, then an invalid -x flag, to exercise both branches of parse
parse -h                 # => runs the -h branch above
echo "exit after -h: $?" # => $? here is parse's return status from the -h call (0)

parse -x && echo "unexpected success" || echo "exit after -x: $?" # => -x is invalid, so the || branch runs
# => $? here is parse's return status (1)
# => Output: usage line, "exit after -h: 0", "invalid option: -x", "exit after -x: 1"
