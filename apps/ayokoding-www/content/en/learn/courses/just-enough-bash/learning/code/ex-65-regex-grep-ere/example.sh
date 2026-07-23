#!/usr/bin/env bash
# Example 65: grep -E with an anchored phone-number pattern
set -euo pipefail

lines=$'555-1234\nhello\n123-4567\nnot-a-number\n42-99'
# => five sample lines; only two are shaped like a 3-digit-dash-4-digit phone number
echo "$lines" | grep -E '^[0-9]{3}-[0-9]{4}$'
# => -E enables extended regex, so {3}/{4} quantifiers work without backslash-escaping
# => ^...$ anchors the match to the WHOLE line, not a substring anywhere within it
# => Output: 555-1234 then 123-4567
