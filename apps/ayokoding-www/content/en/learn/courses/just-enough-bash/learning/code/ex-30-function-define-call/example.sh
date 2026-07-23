#!/usr/bin/env bash
# Example 30: defining and calling a function
set -euo pipefail

greet() {      # => defines a function named greet
  echo "Hi $1" # => prints a greeting using the function's first argument
}              # => closes the function body

greet "Ada" # => calls greet with one argument: "Ada"
# => Output: Hi Ada
