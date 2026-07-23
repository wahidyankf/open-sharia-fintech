#!/usr/bin/env bash
# Example 24: Pin and Remediate a CVE (co-21).
# The SAME requirements.txt as Example 23, with requests bumped from the
# vulnerable 2.19.1 to the current, CVE-clean 2.34.2 -- re-audited for real.
set -euo pipefail # => co-21: -e restored -- a clean audit (exit 0) IS the expected success path here

TARGET_DIR="$(mktemp -d)"                                                       # => co-21: a fresh throwaway install target, self-contained per-run
echo "== Installing the BUMPED requirements.txt into an isolated target dir ==" # => co-21: requests==2.34.2 this time
pip install --quiet --target "$TARGET_DIR" -r requirements.txt                  # => co-21: installs the CVE-clean pin

echo "== pip-audit --path (real, captured output) ==" # => co-21: re-runs the EXACT same check as Example 23
pip-audit --path "$TARGET_DIR"                        # => co-21: audits the packages found in TARGET_DIR against the PyPA Advisory DB
echo "pip-audit exit code: $?"                        # => co-21: 0 means CLEAN -- no known vulnerabilities remain

rm -rf "$TARGET_DIR" # => co-21: cleans up the throwaway install target
