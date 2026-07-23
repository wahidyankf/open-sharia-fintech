#!/usr/bin/env bash
python3 -m pytest -q test_totals.py # => co-09/co-10: exit 0 = good, nonzero = bad -- bisect run's pass/fail oracle
