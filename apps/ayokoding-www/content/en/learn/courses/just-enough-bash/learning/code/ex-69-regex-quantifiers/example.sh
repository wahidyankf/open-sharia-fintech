#!/usr/bin/env bash
# Example 69: grep -E with the + quantifier
set -euo pipefail

printf 'abc\nabbc\nabbbc\nac\n' | grep -E 'ab+c'
# => + means "one or more of the preceding atom" -- here, one or more b characters
# => abc/abbc/abbbc all have at least one b between a and c, so all three match
# => ac has ZERO b characters, so it does not match
# => Output: abc, abbc, abbbc
