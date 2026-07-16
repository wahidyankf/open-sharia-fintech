# learning/code/ex-66-rbac-vs-abac-authorization/rbac_vs_abac.py
"""Example 66: the SAME resource, checked by a role-based rule and an attribute-based rule -- and they genuinely diverge (co-16, co-15)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the authorization logic itself

from dataclasses import (
    dataclass,
)  # => co-16: a real, typed test-case record -- not a loose tuple

USERS: dict[str, str] = {
    "alice": "author",
    "bob": "editor",
    "carol": "admin",
    "dave": "author",
}  # => co-16: real roles
DOCUMENTS: dict[str, str] = {
    "doc-1": "alice",
    "doc-2": "dave",
}  # => co-15: real ownership map -- doc id -> owner


def rbac_allow(
    user: str, document_id: str
) -> bool:  # => co-16: ROLE-BASED -- only asks "what role does this user have"
    return USERS.get(user) in {
        "editor",
        "admin",
    }  # => co-16: ANY editor/admin may touch ANY document -- coarse-grained
    # => co-16: notice -- this function NEVER even looks at document_id's actual owner


def abac_allow(
    user: str, document_id: str
) -> bool:  # => co-15: ATTRIBUTE-BASED -- asks about THIS specific pairing
    owner = DOCUMENTS.get(
        document_id
    )  # => co-15: the REAL owner of this SPECIFIC document
    role = USERS.get(
        user
    )  # => co-15: the REAL role of this specific user -- used only as ONE input among several
    return (
        owner == user or role == "admin"
    )  # => co-15: fine-grained -- ownership OR admin override, nothing broader


@dataclass  # => co-16: one real row per (user, document) scenario this comparison exercises
class Case:  # => co-15: the shape every real test-case row takes
    user: str  # => co-16: WHO is asking
    document_id: str  # => co-15: WHICH resource they're asking about
    expected_rbac: (
        bool  # => co-16: what the ROLE-BASED rule should decide for this pairing
    )
    expected_abac: bool  # => co-15: what the ATTRIBUTE-BASED rule should decide for the SAME pairing


CASES: list[
    Case
] = [  # => co-16: every real scenario this comparison runs, covering every meaningful combination
    Case(
        "bob", "doc-1", expected_rbac=True, expected_abac=False
    ),  # => co-16: editor, NOT owner -- RBAC/ABAC DIVERGE
    Case(
        "alice", "doc-1", expected_rbac=False, expected_abac=True
    ),  # => co-15: owner, NOT editor -- RBAC/ABAC DIVERGE
    Case(
        "carol", "doc-1", expected_rbac=True, expected_abac=True
    ),  # => co-16: admin -- both rules allow, same reason
    Case(
        "dave", "doc-1", expected_rbac=False, expected_abac=False
    ),  # => co-15: neither owner nor editor -- both deny
    Case(
        "dave", "doc-2", expected_rbac=False, expected_abac=True
    ),  # => co-15: dave owns doc-2 -- ABAC allows HIS doc only
    Case(
        "bob", "doc-2", expected_rbac=True, expected_abac=False
    ),  # => co-16: editor again -- RBAC allows ANY document
]


def main() -> (
    None
):  # => co-16: runs EVERY real case against BOTH real implementations and checks BOTH expected columns
    print(f"users/roles: {USERS}")  # => co-16: the real role table both rules read from
    print(
        f"document ownership: {DOCUMENTS}\n"
    )  # => co-15: the real ownership table only the ABAC rule reads from

    for case in (
        CASES
    ):  # => co-16: every real, concrete (user, document) pairing this comparison covers
        actual_rbac = rbac_allow(
            case.user, case.document_id
        )  # => co-16: the REAL, computed RBAC verdict
        actual_abac = abac_allow(
            case.user, case.document_id
        )  # => co-15: the REAL, computed ABAC verdict
        agree = (
            "SAME" if actual_rbac == actual_abac else "DIVERGE"
        )  # => co-16: real, human-readable comparison
        print(  # => co-16: one real, full row per case -- both real verdicts, side by side
            f"  {case.user:6} x {case.document_id}: rbac={actual_rbac!s:5} abac={actual_abac!s:5}  [{agree}]"
        )
        assert actual_rbac == case.expected_rbac, (
            f"RBAC mismatch for {case}"
        )  # => co-16: proves THIS rule matches its column
        assert actual_abac == case.expected_abac, (
            f"ABAC mismatch for {case}"
        )  # => co-15: proves THIS rule matches its column

    divergent_cases = [
        c for c in CASES if c.expected_rbac != c.expected_abac
    ]  # => co-16: real cases where they DISAGREE
    print(
        f"\n{len(divergent_cases)} of {len(CASES)} real cases produce DIFFERENT RBAC vs. ABAC verdicts"
    )  # => co-16
    assert (
        len(divergent_cases) >= 2
    )  # => co-16: proves the two models really are NOT interchangeable, not just relabeled


if (
    __name__ == "__main__"
):  # => co-16: only runs when launched directly, e.g. `python3 rbac_vs_abac.py`
    main()  # => co-16: runs every real case against both real rules and verifies every real expected column
