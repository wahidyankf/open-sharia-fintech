#!/usr/bin/env bash
# Example 13: Exit Code Failure
false     # => the `false` builtin always fails, setting $? to 1
echo "$?" # => $? reports the previous command's exit status
# => Output: 1
