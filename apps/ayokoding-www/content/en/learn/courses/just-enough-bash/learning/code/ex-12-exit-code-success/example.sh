#!/usr/bin/env bash
# Example 12: Exit Code Success
true      # => the `true` builtin always succeeds, setting $? to 0
echo "$?" # => $? holds the exit status of the immediately preceding command
# => Output: 0
