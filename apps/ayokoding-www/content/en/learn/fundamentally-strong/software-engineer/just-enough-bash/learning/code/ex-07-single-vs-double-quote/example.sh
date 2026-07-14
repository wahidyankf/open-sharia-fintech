#!/usr/bin/env bash
# Example 7: Single Vs Double Quote
name="Ada" # => assigns Ada to name
# shellcheck disable=SC2016 # => intentional: this line demonstrates that single quotes do NOT expand
echo '$name' # => single quotes are literal: no expansion happens
# => Output line 1: $name
echo "$name" # => double quotes allow expansion: $name becomes Ada
# => Output line 2: Ada
