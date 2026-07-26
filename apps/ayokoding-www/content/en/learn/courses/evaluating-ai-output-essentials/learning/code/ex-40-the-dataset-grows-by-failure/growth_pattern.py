# learning/code/ex-40-the-dataset-grows-by-failure/growth_pattern.py
"""Worked Example 40: The Dataset Grows by Failure."""  # => co-10: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

CASE_LOG = [  # => co-10: every case ever added, in commit order, each tagged with WHY it was added
    {"id": "case-01", "source": "initial-collection"},  # => co-03: the original ten
    {"id": "case-02", "source": "initial-collection"},  # => co-03: the original ten
    {"id": "case-03", "source": "initial-collection"},  # => co-03: cases 3-4
    {"id": "case-04", "source": "initial-collection"},  # => co-03: cases 3-4
    {"id": "case-05", "source": "initial-collection"},  # => co-03: cases 5-6
    {"id": "case-06", "source": "initial-collection"},  # => co-03: cases 5-6
    {"id": "case-07", "source": "initial-collection"},  # => co-03: cases 7-8
    {"id": "case-08", "source": "initial-collection"},  # => co-03: cases 7-8
    {"id": "case-09", "source": "initial-collection"},  # => co-03: cases 9-10
    {"id": "case-10", "source": "initial-collection"},  # => co-03: cases 9-10
    {"id": "case-13", "source": "bug-report"},  # => co-10: added later -- sourced from a REAL reported failure (ex-39)
    {"id": "case-14", "source": "bug-report"},  # => co-10: added later -- sourced from a second real reported failure
]  # => co-10: closes CASE_LOG
ALLOWED_GROWTH_SOURCES = {"bug-report"}  # => co-10: after the initial collection, ONLY this source may add a case


def cases_added_after_initial(log: list[dict[str, str]]) -> list[dict[str, str]]:  # => co-10: everything past the founding set
    """Return every log entry whose source is not 'initial-collection'."""  # => co-10: documents cases_added_after_initial's contract -- no runtime output, just sets its __doc__
    return [entry for entry in log if entry["source"] != "initial-collection"]  # => co-10: the dataset's growth history


if __name__ == "__main__":  # => co-10: entry point -- runs only when this file executes directly, not on import
    grown_entries = cases_added_after_initial(CASE_LOG)  # => co-10: every case added after day one
    print(f"Cases added after initial collection: {[e['id'] for e in grown_entries]}")  # => co-10: prints the growth list
    grown_sources = {entry["source"] for entry in grown_entries}  # => co-10: which sources actually contributed growth
    print(f"Sources of growth: {sorted(grown_sources)}")  # => co-10: prints the distinct sources seen
    assert grown_sources <= ALLOWED_GROWTH_SOURCES, "every case added after the initial set must trace to a real bug report"  # => co-10
    assert len(grown_entries) == 2, "exactly two cases must have been added by this point in the log"  # => co-10: sanity check
    print("MATCH: every case added past day one traces to something a real user actually hit")  # => co-10
    # => co-10: this discipline is how a ten-case gate becomes a genuinely useful dataset without ever becoming speculative
