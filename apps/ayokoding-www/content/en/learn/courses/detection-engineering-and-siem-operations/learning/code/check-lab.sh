#!/usr/bin/env sh
set -eu
# => This verifier has no host argument and reads only files in this course's code directory.
python3 "$(dirname "$0")/detection_lab.py" verify
