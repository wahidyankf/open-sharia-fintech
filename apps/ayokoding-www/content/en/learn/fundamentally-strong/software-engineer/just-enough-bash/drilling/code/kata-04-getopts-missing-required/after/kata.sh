#!/usr/bin/env bash
set -euo pipefail
# Kata 4 (FIXED): explicitly validates that -i was supplied, with a clear
# usage message, before ever touching $input.
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

if [ -z "$input" ]; then
  echo "kata.sh: -i <input> is required" >&2
  exit 1
fi

echo "reading from: '$input'"
wc -l <"$input"
