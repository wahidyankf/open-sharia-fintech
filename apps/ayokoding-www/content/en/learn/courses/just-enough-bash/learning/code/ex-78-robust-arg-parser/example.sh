#!/usr/bin/env bash
# Example 78: a robust getopts parser with required-option validation
set -euo pipefail # => same strict-mode header as every other example in this primer

usage() { echo "usage: example.sh -i <input>" >&2; } # => usage text goes to stderr, the conventional channel

input=""                                                        # => default: empty means "not yet provided" -- getopts alone cannot enforce -i is REQUIRED
while getopts ":i:h" opt; do                                    # => leading : enables SILENT error handling; i: takes a value, h takes none
  case "$opt" in                                                # => $opt holds the option letter getopts just parsed
  i) input="$OPTARG" ;;                                         # => records the value that followed -i
  h)                                                            # => matches when -h was passed
    usage                                                       # => prints the one-line usage text
    exit 0                                                      # => -h always exits successfully (status 0)
    ;;                                                          # => ends this branch
  \?)                                                           # => matches any option NOT in ":i:h" -- an invalid flag
    echo "example.sh: invalid option -$OPTARG" >&2              # => $OPTARG holds the invalid letter
    usage                                                       # => reminds the caller of correct usage
    exit 1                                                      # => an invalid option is a hard failure
    ;;                                                          # => ends this branch
  :)                                                            # => matches a value-taking option (-i) given no value
    echo "example.sh: option -$OPTARG requires an argument" >&2 # => $OPTARG holds the letter missing a value
    usage                                                       # => reminds the caller of correct usage
    exit 1                                                      # => a missing required value is also fatal
    ;;                                                          # => ends this branch
  esac                                                          # => closes the case statement
done                                                            # => closes the while-loop; getopts returns non-zero once options are exhausted

if [[ -z "$input" ]]; then
  # => this manual check is what actually enforces -i as REQUIRED, since getopts treats every flag as optional
  echo "example.sh: -i is required" >&2 # => -i was never provided, or was provided as an empty string
  usage                                 # => reminds the caller of correct usage
  exit 1                                # => missing a REQUIRED option is a hard failure, not a warning
fi                                      # => closes the if

echo "input: $input" # => reached only when -i was provided with a real value
# => Output (when -i is provided): input: <value>
