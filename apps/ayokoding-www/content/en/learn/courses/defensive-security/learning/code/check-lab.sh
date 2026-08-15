#!/usr/bin/env sh
set -eu
# => This offline check passes no endpoint, host, or user input to the Python lab.
python3 "$(dirname "$0")/blue_lab.py" verify
