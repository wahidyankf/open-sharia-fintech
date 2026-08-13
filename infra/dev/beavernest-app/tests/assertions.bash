#!/usr/bin/env bash

assert_no_match() {
  local status

  if "$@"; then
    return 1
  fi

  status=$?
  [[ "$status" -eq 1 ]] || return "$status"
}
