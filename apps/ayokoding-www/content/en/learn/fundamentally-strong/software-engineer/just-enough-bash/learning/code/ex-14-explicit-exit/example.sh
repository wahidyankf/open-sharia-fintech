#!/usr/bin/env bash
# Example 14: Explicit Exit
echo "about to exit" # => runs before the explicit exit below
# => Output line 1: about to exit
exit 3 # => sets the script's own exit status to 3, overriding the default of 0
