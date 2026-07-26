# learning/code/ex-14-regex-scorer/regex_scorer.py
"""Worked Example 14: Regex Scorer."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import re  # => co-05: pattern matching needs nothing beyond the standard library's own re module

TICKET_ID_PATTERN = re.compile(r"TCK-\d{6}")  # => co-05: co-04's format requirement -- "TCK-" plus exactly six digits


def regex_scorer(output: str, pattern: re.Pattern[str]) -> bool:  # => co-05: for a required FORMAT, not a required literal
    """Pass iff `pattern` matches somewhere inside `output`."""  # => co-05: documents regex_scorer's contract -- no runtime output, just sets its __doc__
    return pattern.search(output) is not None  # => co-05: search, not match -- the pattern may sit anywhere in the text


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    well_formed = "Your support ticket has been opened as TCK-004821 -- we'll follow up soon."  # => co-05: matches the format
    malformed = "Your support ticket has been opened as ticket #4821 -- we'll follow up soon."  # => co-05: WRONG format, same info
    well_formed_result = regex_scorer(well_formed, TICKET_ID_PATTERN)  # => co-05: the pass path
    malformed_result = regex_scorer(malformed, TICKET_ID_PATTERN)  # => co-05: the fail path -- format violated
    print(f"regex_scorer(well_formed, TICKET_ID_PATTERN) = {well_formed_result}")  # => co-05: prints the pass verdict
    print(f"regex_scorer(malformed, TICKET_ID_PATTERN) = {malformed_result}")  # => co-05: prints the fail verdict
    assert well_formed_result is True, "a correctly-formatted ticket id must pass"  # => co-05: confirms the pass path
    assert malformed_result is False, "a differently-formatted ticket id must fail, even with the same information"  # => co-05
    print("MATCH: regex scoring catches format violations a substring check would miss entirely")  # => co-05
    # => co-05: any downstream system parsing this output by regex needs the FORMAT enforced, not just the content
