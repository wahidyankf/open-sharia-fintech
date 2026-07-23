#!/usr/bin/env bash
# Example 27: Redirect Stderr
ls /no-such-path-xyz 2>err.txt # => 2> captures only stderr (fd 2) into err.txt; stdout (fd 1) is untouched
# => ls finds nothing, so its own stdout stays empty -- no output here
cat err.txt # => Output: the captured error text (verifies err.txt is non-empty)
