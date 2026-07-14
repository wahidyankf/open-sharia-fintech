#!/usr/bin/env bash
# Example 56: parsing flags with getopts
set -euo pipefail

set -- -v -o result.txt # => simulates script arguments: a flag (-v) and a flag with a value (-o result.txt)

verbose="false" # => default value, overwritten only if -v is present
outfile=""      # => default value, overwritten only if -o is present

while getopts "vo:" opt; do # => "vo:" declares flag -v (no value) and flag -o (colon means it TAKES a value)
  case "$opt" in            # => $opt holds the option letter getopts just parsed
  v)                        # => matches when -v was passed
    verbose="true"          # => records that verbose mode was requested
    ;;                      # => ends this branch
  o)                        # => matches when -o was passed
    outfile="$OPTARG"       # => $OPTARG holds the value that followed -o (here, "result.txt")
    ;;                      # => ends this branch
  *) ;;                     # => catch-all for any other option; nothing to do here
  esac                      # => closes the case statement
done                        # => closes the while-loop; getopts returns non-zero once options are exhausted

echo "verbose: $verbose" # => shows the flag was recorded
echo "outfile: $outfile" # => shows the flag's value was captured
# => Output: "verbose: true" then "outfile: result.txt"
