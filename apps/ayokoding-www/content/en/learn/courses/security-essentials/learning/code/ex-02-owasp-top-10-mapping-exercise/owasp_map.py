# learning/code/ex-02-owasp-top-10-mapping-exercise/owasp_map.py
"""Example 2: OWASP Top 10 Mapping Exercise."""  # => co-02: module docstring, shown in help(module)

from __future__ import (
    annotations,
)  # => co-02: DD-39 hygiene for the `list[SeededBug]` annotation below

from typing import (
    NamedTuple,
)  # => co-02: a typed tuple names each field instead of a bare 3-tuple


class SeededBug(
    NamedTuple
):  # => co-02: one seeded bug, its own OWASP category, and why
    description: (
        str  # => a one-line description of the concrete bug found in the sample app
    )
    owasp_id: (
        str  # => co-02: the OWASP Top 10:2025 category id this bug maps to (e.g. "A05")
    )
    owasp_name: str  # => co-02: the human-readable category name for owasp_id
    reason: str  # => co-02: WHY this bug maps to that category, not a different one


# ex-02: five bugs seeded into a small sample app, each mapped to its OWASP
# Top 10:2025 category -- the shared risk vocabulary this whole topic is organized around
SEEDED_BUGS: list[
    SeededBug
] = [  # => co-02: 5 rows, each independently verified below by an assert
    SeededBug(  # => bug #1: injection
        "login query built with an f-string: f\"SELECT ... WHERE user='{u}'\"",  # => the bug itself
        "A05",
        "Injection",  # => co-02: untrusted input becomes part of the SQL command
        "attacker input changes the STRUCTURE of a command, the textbook injection pattern",  # => why
    ),  # => end bug #1
    SeededBug(  # => bug #2: misconfiguration
        "Flask app runs with debug=True and the interactive debugger reachable in prod",  # => the bug
        "A02",
        "Security Misconfiguration",  # => co-02: an insecure DEFAULT, not a coding mistake
        "the framework's own default (debug mode) is left on where it should be off",  # => why
    ),  # => end bug #2
    SeededBug(  # => bug #3: supply chain
        "requirements.txt pins Flask==0.12.2, a version with a public disclosed CVE",  # => the bug
        "A03",
        "Software Supply Chain Failures",  # => co-02: risk lives in a THIRD-PARTY dependency
        "the vulnerable code is not the app's own -- it is an unpatched dependency",  # => why
    ),  # => end bug #3
    SeededBug(  # => bug #4: crypto failure
        "passwords stored as unsalted hashlib.md5(password).hexdigest()",  # => the bug
        "A04",
        "Cryptographic Failures",  # => co-02: a weak/misused cryptographic primitive
        "MD5 is a fast, unsalted hash -- exactly the cryptographic failure this category names",  # => why
    ),  # => end bug #4
    SeededBug(  # => bug #5: access control
        "GET /orders/<id> returns ANY order for ANY logged-in user, no ownership check",  # => the bug
        "A01",
        "Broken Access Control",  # => co-02: a missing authorization check, not authentication
        "the user IS authenticated -- the missing check is WHOSE data they may read",  # => why
    ),  # => end bug #5
]  # => co-02: end of the 5-row seeded-bug table

# ex-02: an independent grader, built WITHOUT looking at SEEDED_BUGS above, used
# only to verify each row's tag is internally consistent (id and name actually match)
VALID_CATEGORIES: dict[
    str, str
] = {  # => co-02: the closed OWASP Top 10:2025 vocabulary, id -> name
    "A01": "Broken Access Control",  # => co-02: valid id/name pair #1
    "A02": "Security Misconfiguration",  # => co-02: valid id/name pair #2
    "A03": "Software Supply Chain Failures",  # => co-02: valid id/name pair #3
    "A04": "Cryptographic Failures",  # => co-02: valid id/name pair #4
    "A05": "Injection",  # => co-02: valid id/name pair #5
}  # => co-02: end of the closed vocabulary dict


def verify_tags(
    bugs: list[SeededBug],
) -> None:  # => co-02: raises if any row's id/name pair is inconsistent
    """Confirm every bug's owasp_id and owasp_name are a REAL, matching OWASP Top 10:2025 pair."""  # => doc
    for bug in bugs:  # => co-02: checked independently, one bug at a time
        assert bug.owasp_id in VALID_CATEGORIES, (
            f"unknown id {bug.owasp_id!r}"
        )  # => co-02: id must exist
        assert VALID_CATEGORIES[bug.owasp_id] == bug.owasp_name, (
            "id/name mismatch"
        )  # => co-02: names agree


if (
    __name__ == "__main__"
):  # => co-02: entry point -- verify, then print each tagged bug
    verify_tags(
        SEEDED_BUGS
    )  # => co-02: raises AssertionError immediately if any tag is wrong -- none are
    for i, bug in enumerate(
        SEEDED_BUGS, start=1
    ):  # => co-02: one printed block per seeded bug
        print(
            f"Bug {i}: {bug.description}"
        )  # => co-02: the concrete symptom found in the sample app
        print(
            f"  -> {bug.owasp_id} {bug.owasp_name}"
        )  # => co-02: the category id this bug is tagged with
        print(
            f"     because: {bug.reason}"
        )  # => co-02: the justification a reviewer can check
    print(
        f"\nAll {len(SEEDED_BUGS)} bugs verified against {len(VALID_CATEGORIES)} OWASP categories."
    )  # => co-02: summary
