#!/usr/bin/env bash
# Example 77: shfmt formats inconsistent indentation
set -euo pipefail     # => same strict-mode header as every other example in this primer
if true; then         # => a trivial condition, just to give shfmt an indented block to fix
  echo "inconsistent" # => before shfmt -w, this line and the one below had mismatched indentation
  echo "spacing"      # => shfmt -w normalizes both lines to this topic's 2-space .editorconfig setting
fi                    # => closes the if
# => this fixed, shfmt-clean version is exactly what a reader has on disk after following this example
