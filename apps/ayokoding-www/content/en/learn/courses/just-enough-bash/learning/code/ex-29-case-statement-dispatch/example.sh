#!/usr/bin/env bash
# Example 29: case statement -- dispatching on an action word
set -euo pipefail

dispatch() {                  # => dispatch takes one action word and routes it
  case "$1" in                # => case matches $1 against each pattern below, top to bottom
  start)                      # => matches the literal word "start"
    echo "starting service"   # => branch body: runs only for the start case
    ;;                        # => ;; ends this branch and skips every other pattern
  stop)                       # => matches the literal word "stop"
    echo "stopping service"   # => branch body: runs only for the stop case
    ;;                        # => ;; ends this branch
  *)                          # => * is the catch-all pattern, matches anything else
    echo "unknown action: $1" # => branch body for every action that is not start or stop
    ;;                        # => ;; ends the catch-all branch
  esac                        # => esac closes the case statement
}                             # => closes the dispatch function

for action in start stop restart; do # => drives dispatch with three sample inputs
  dispatch "$action"                 # => calls dispatch, routing through case each time
done                                 # => closes the for-loop
# => Output: "starting service", then "stopping service", then "unknown action: restart"
