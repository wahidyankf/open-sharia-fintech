# learning/code/ex-60-threat-model-a-feature/threat_model.py
"""Example 60: a real STRIDE-lite pass over the login endpoint from ex-46/ex-48, each threat tied to a named control (co-25, co-02)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the STRIDE enumeration itself

import re  # => co-02: verifies every real mitigation cites a REAL co-NN/ex-NN reference, not just prose
from dataclasses import (
    dataclass,
)  # => co-02: a real, typed record -- not a loose dict per threat


@dataclass  # => co-02: one real, structured entry per STRIDE category -- forces every field to be filled in
class ThreatEntry:  # => co-25: the SHAPE every threat-model row must take -- category, threat, and its real control
    category: str  # => co-02: one of the six real STRIDE letters -- S, T, R, I, D, or E
    threat: str  # => co-25: a CONCRETE threat against the login endpoint -- not a generic description
    mitigating_control: str  # => co-25: the REAL, specific control this topic already implements that stops it
    cites: str  # => co-02: the real co-NN/ex-NN reference backing the mitigating_control claim


# => co-25: target feature for this pass -- the login endpoint from ex-46 (rate limiting) / ex-48
# => (constant-time response) / ex-15 (argon2id hashing), analyzed for real, one row per STRIDE letter
LOGIN_ENDPOINT_THREAT_MODEL: list[ThreatEntry] = [
    ThreatEntry(  # => co-02: S -- Spoofing
        category="Spoofing",
        threat="an attacker submits a forged or stolen session cookie to impersonate a real user",
        mitigating_control="session id regenerated on login, unguessable via secrets.token_urlsafe",
        cites="co-12, ex-36",
    ),
    ThreatEntry(  # => co-02: T -- Tampering
        category="Tampering",
        threat="an attacker modifies a JWT's claims (e.g. role) in transit to escalate privilege",
        mitigating_control="signature verification with a pinned algorithm rejects any modified token",
        cites="co-14, ex-38",
    ),
    ThreatEntry(  # => co-02: R -- Repudiation
        category="Repudiation",
        threat="a user denies attempting (or succeeding at) a login after the fact",
        mitigating_control="structured JSON authn logging records user/action/outcome for every attempt",
        cites="co-22, ex-57",
    ),
    ThreatEntry(  # => co-02: I -- Information Disclosure
        category="Information Disclosure",
        threat="response timing reveals whether a submitted username exists at all",
        mitigating_control="constant-time login always hashes a dummy for unknown usernames too",
        cites="co-11, ex-48",
    ),
    ThreatEntry(  # => co-02: D -- Denial of Service
        category="Denial of Service",
        threat="an attacker submits unlimited login attempts per second, exhausting resources",
        mitigating_control="flask-limiter throttles each caller to a fixed rate, returning 429 past it",
        cites="co-27, ex-46",
    ),
    ThreatEntry(  # => co-02: E -- Elevation of Privilege
        category="Elevation of Privilege",
        threat="a non-admin, authenticated user reaches an admin-only route by guessing its URL",
        mitigating_control="a require_admin check runs server-side on every request to that route",
        cites="co-16, ex-34",
    ),
]

STRIDE_CATEGORIES = {  # => co-02: the real, canonical six STRIDE category names -- the full checklist this pass covers
    "Spoofing",
    "Tampering",
    "Repudiation",
    "Information Disclosure",
    "Denial of Service",
    "Elevation of Privilege",
}


def main() -> (
    None
):  # => co-02: prints the real threat model, then verifies every real completeness invariant
    print(
        "=== STRIDE-lite pass: the login endpoint (ex-46/ex-48/ex-15) ===\n"
    )  # => labels section
    for entry in (
        LOGIN_ENDPOINT_THREAT_MODEL
    ):  # => co-02: every REAL row this pass produced, in STRIDE order
        print(
            f"[{entry.category}]"
        )  # => co-02: the real STRIDE letter this row addresses
        print(
            f"  threat:     {entry.threat}"
        )  # => co-25: the real, concrete threat -- not a generic placeholder
        print(
            f"  mitigation: {entry.mitigating_control}"
        )  # => co-25: the real, already-implemented control
        print(
            f"  cites:      {entry.cites}\n"
        )  # => co-02: the real co-NN/ex-NN this claim is traceable back to

    categories_covered = {
        entry.category for entry in LOGIN_ENDPOINT_THREAT_MODEL
    }  # => co-02: the real set covered
    assert (
        categories_covered == STRIDE_CATEGORIES
    )  # => co-02: proves ALL SIX real STRIDE categories are represented
    assert (
        len(LOGIN_ENDPOINT_THREAT_MODEL) == 6
    )  # => co-02: proves exactly one row per category -- no duplicates

    cite_pattern = re.compile(
        r"co-\d{2}"
    )  # => co-02: the real, expected shape of a concept citation
    for (
        entry
    ) in LOGIN_ENDPOINT_THREAT_MODEL:  # => co-02: verifies EVERY real row, not a sample
        assert cite_pattern.search(entry.cites), (
            f"{entry.category} is missing a real co-NN citation"
        )  # => co-02: real check
        assert (
            entry.mitigating_control.strip() != ""
        )  # => co-25: proves every threat really has a real, non-empty control
    print(
        "verified: all 6 STRIDE categories present, each with a real co-NN-cited mitigation"
    )  # => co-02: real conclusion


if (
    __name__ == "__main__"
):  # => co-02: only runs when launched directly, e.g. `python3 threat_model.py`
    main()  # => co-02: prints the real, full threat model and verifies every real completeness invariant
