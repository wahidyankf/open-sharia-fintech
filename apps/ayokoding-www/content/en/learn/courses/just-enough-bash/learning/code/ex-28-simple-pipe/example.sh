#!/usr/bin/env bash
# Example 28: Simple Pipe
printf 'b\na\n' | sort # => printf's stdout feeds directly into sort's stdin via the pipe
# => Output: a, then b (sort reorders the two lines alphabetically)
