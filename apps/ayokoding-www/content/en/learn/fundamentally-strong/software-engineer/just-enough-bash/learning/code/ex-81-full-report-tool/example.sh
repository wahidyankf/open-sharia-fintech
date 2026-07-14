#!/usr/bin/env bash
# Example 81: full-report-tool -- getopts + text pipeline + trap/mktemp + exit codes
set -euo pipefail # => same strict-mode header as every other example in this primer

usage() { echo "usage: example.sh -i <input> -o <output>" >&2; } # => shared one-line usage text

input=""  # => default: empty means -i was not provided
output="" # => default: empty means -o was not provided

while getopts ":i:o:h" opt; do                                  # => leading : enables SILENT error handling for invalid/missing-value flags
  case "$opt" in                                                # => $opt holds the option letter getopts just parsed
  i) input="$OPTARG" ;;                                         # => records the value that followed -i
  o) output="$OPTARG" ;;                                        # => records the value that followed -o
  h)                                                            # => matches when -h was passed
    usage                                                       # => prints the shared usage text
    exit 0                                                      # => -h always exits successfully
    ;;                                                          # => ends this branch
  \?)                                                           # => matches any option NOT in ":i:o:h"
    echo "example.sh: invalid option -$OPTARG" >&2              # => $OPTARG holds the invalid letter
    usage                                                       # => reminds the caller of correct usage
    exit 1                                                      # => an invalid option is a hard failure
    ;;                                                          # => ends this branch
  :)                                                            # => matches a value-taking option given no value
    echo "example.sh: option -$OPTARG requires an argument" >&2 # => $OPTARG holds the letter missing a value
    usage                                                       # => reminds the caller of correct usage
    exit 1                                                      # => a missing required value is also fatal
    ;;                                                          # => ends this branch
  esac                                                          # => closes the case statement
done                                                            # => closes the while-loop

if [[ -z "$input" || -z "$output" ]]; then
  # => a manual check, since getopts alone cannot enforce that -i AND -o are both REQUIRED
  echo "example.sh: -i and -o are both required" >&2 # => neither flag was fully provided
  usage                                              # => reminds the caller of correct usage
  exit 1                                             # => missing a required option/value is a hard failure
fi                                                   # => closes the if

if [[ ! -f "$input" ]]; then                          # => -i was provided, but the path it names does not actually exist
  echo "example.sh: input file not found: $input" >&2 # => reported on stderr, the conventional channel
  exit 1                                              # => a nonexistent input file is also a hard failure
fi                                                    # => closes the if

scratch="$(mktemp)"          # => private scratch file; the real report is built here first
trap 'rm -f "$scratch"' EXIT # => a validation or pipeline failure above never leaves scratch behind

grep -Eo '\b(INFO|WARN|ERROR)\b' "$input" | # => extracts just the level word from each log line
  sort |                                    # => groups identical levels together, a prerequisite for uniq
  uniq -c |                                 # => counts how many times each level occurs
  sort -rn >"$scratch"                      # => most frequent level first

mv "$scratch" "$output" # => atomic: $output either has the complete report, or the run failed before this
echo "wrote: $output"   # => confirms the atomic publish succeeded
