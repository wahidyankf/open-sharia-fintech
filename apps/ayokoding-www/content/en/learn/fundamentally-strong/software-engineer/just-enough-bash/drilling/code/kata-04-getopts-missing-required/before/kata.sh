#!/usr/bin/env bash
set -euo pipefail
# Kata 4 (BUGGY): parses -i but never checks it was actually supplied,
# so running the script with no options at all silently proceeds with an
# empty $input and fails later with a confusing, unrelated error.
input=""
while getopts ":i:" opt; do
  case "$opt" in
  i) input="$OPTARG" ;;
  *)
    echo "usage: kata.sh -i <input>" >&2
    exit 1
    ;;
  esac
done

echo "reading from: '$input'"
wc -l <"$input"
