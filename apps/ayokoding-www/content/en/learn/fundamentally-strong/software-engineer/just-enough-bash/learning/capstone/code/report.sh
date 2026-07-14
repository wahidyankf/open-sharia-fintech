#!/usr/bin/env bash
# report.sh -- Just Enough Bash capstone: a word-frequency report tool.
# Combines every mechanism this primer taught: strict mode, getopts, safe
# quoting, a grep/tr/sort/uniq pipeline, mktemp + trap cleanup, and correct
# exit codes.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: report.sh -i <input> -o <output>
  -i <input>   path to the input text file to analyze (required)
  -o <output>  path to write the word-frequency report to (required)
  -h           show this help message and exit
EOF
}

input=""
output=""

while getopts ":i:o:h" opt; do
  case "$opt" in
  i) input="$OPTARG" ;;
  o) output="$OPTARG" ;;
  h)
    usage
    exit 0
    ;;
  \?)
    echo "report.sh: invalid option -$OPTARG" >&2
    usage >&2
    exit 1
    ;;
  :)
    echo "report.sh: option -$OPTARG requires an argument" >&2
    usage >&2
    exit 1
    ;;
  esac
done

if [[ -z "$input" || -z "$output" ]]; then
  echo "report.sh: -i and -o are both required" >&2
  usage >&2
  exit 1
fi

if [[ ! -f "$input" ]]; then
  echo "report.sh: input file not found: $input" >&2
  exit 1
fi

# scratch is created only once both args are validated, so a validation
# failure above never leaves a scratch file behind.
scratch="$(mktemp)"
trap 'rm -f "$scratch"' EXIT
# trap runs on ANY exit (normal or error); rm -f is a silent no-op once the
# final mv below has already moved scratch out from under this path.

tr '[:upper:]' '[:lower:]' <"$input" | # normalize case so "The"/"the" count together
  tr -cs '[:alpha:]' '\n' |            # squeeze every non-letter run into one newline -> one word per line
  grep -v '^$' |                       # drop any leftover empty lines
  sort |                               # group identical words together for uniq
  uniq -c |                            # count each word's occurrences
  sort -rn >"$scratch"                 # most frequent word first

mv "$scratch" "$output" # atomic: report.sh's caller never sees a half-written -o file
