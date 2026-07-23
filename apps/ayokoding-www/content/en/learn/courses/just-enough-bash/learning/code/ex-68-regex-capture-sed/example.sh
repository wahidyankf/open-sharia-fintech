#!/usr/bin/env bash
# Example 68: sed -E with a backreference to a captured group
set -euo pipefail

echo "foobar" | sed -E 's/(foo)bar/\1baz/'
# => (foo) captures "foo" into GROUP 1; \1 in the replacement replays that captured text
# => the match itself, "foobar", is replaced by "foo" (from \1) followed by literal "baz"
# => Output: foobaz
