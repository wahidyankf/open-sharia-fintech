#!/usr/bin/env bash

assert_no_match() {
  local result

  if "$@"; then
    return 1
  else
    result=$?
  fi

  [[ "$result" -eq 1 ]] || return "$result"
}
