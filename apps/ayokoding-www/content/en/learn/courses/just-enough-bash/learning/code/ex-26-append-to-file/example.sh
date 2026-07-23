#!/usr/bin/env bash
# Example 26: Append To File
echo "hi" >out.txt    # => > truncates/creates out.txt with the first line
echo "more" >>out.txt # => >> appends a second line without erasing the first
cat out.txt           # => Output line 1: hi
# => Output line 2: more
