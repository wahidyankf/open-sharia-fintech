#!/usr/bin/env bash
# Example 25: Redirect To File
echo "hi" >out.txt # => > truncates (or creates) out.txt and writes echo's stdout into it
cat out.txt        # => reads out.txt back so the redirected content is visible
# => Output: hi
