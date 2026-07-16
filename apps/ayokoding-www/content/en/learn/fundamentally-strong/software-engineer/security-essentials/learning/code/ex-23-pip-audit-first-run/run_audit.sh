#!/usr/bin/env bash
# Example 23: pip-audit First Run (co-21).
# Installs the pinned requirements.txt into an isolated target directory (no venv
# construction needed -- `pip install --target` places packages directly in a
# folder), then runs `pip-audit --path` against that directory for real.
set -uo pipefail # => co-21: -e omitted deliberately -- pip-audit exits 1 when it FINDS vulnerabilities, which is the expected/success path for this example, not a failure to abort on

TARGET_DIR="$(mktemp -d)"                                            # => co-21: a throwaway install target, self-contained per-run
echo "== Installing requirements.txt into an isolated target dir ==" # => co-21: no real venv, just a plain directory
pip install --quiet --target "$TARGET_DIR" -r requirements.txt       # => co-21: installs ONLY requests + its own deps

echo "== pip-audit --path (real, captured output) ==" # => co-21: the actual verification this example proves
pip-audit --path "$TARGET_DIR"                        # => co-21: audits the packages found in TARGET_DIR against the PyPA Advisory DB
echo "pip-audit exit code: $?"                        # => co-21: 1 means vulnerabilities WERE found -- the expected result here

rm -rf "$TARGET_DIR" # => co-21: cleans up the throwaway install target
