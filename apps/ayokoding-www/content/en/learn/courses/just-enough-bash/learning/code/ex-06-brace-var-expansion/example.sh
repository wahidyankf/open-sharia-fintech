#!/usr/bin/env bash
# Example 6: Brace Var Expansion
name="Ada"        # => assigns Ada to name
echo "Hi ${name}" # => ${name} is the braced expansion form, identical to $name here
# => braces matter when text follows directly, e.g. "${name}s"
# => Output: Hi Ada
