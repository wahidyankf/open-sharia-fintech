"""Consume data delivered through standard input."""

import io
import sys

original = sys.stdin
try:
    sys.stdin = io.StringIO("first note\n")
    print(sys.stdin.read().strip())
finally:
    sys.stdin = original
