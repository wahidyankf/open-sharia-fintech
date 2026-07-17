"""Capstone -- Sequential Transaction Processor, implemented in four paradigms.

Problem: given a starting balance and an ordered list of transaction amounts (positive =
deposit, negative = withdrawal), apply each transaction in order. A transaction that would
drive the balance negative is REJECTED (skipped; balance stays unchanged for that step) rather
than applied. Return the final balance and the list of rejected transaction indices.

All four submodules (imperative, oo, functional, reactive) solve this identical problem and are
verified against the identical expected result in tests/test_shared.py.
"""
