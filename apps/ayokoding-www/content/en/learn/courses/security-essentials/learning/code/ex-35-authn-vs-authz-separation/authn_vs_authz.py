"""Example 35: authentication and authorization as two distinct, separately-named checks (co-15)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the authn/authz separation itself

from dataclasses import (
    dataclass,
)  # => co-15: a real typed value object -- not a bare dict of "who is this"


@dataclass  # => co-15: an immutable-by-convention record of a real authenticated session
class Session:  # => co-15: the OUTPUT of authentication -- proof of identity, nothing about permission yet
    user_id: str  # => co-15: WHO this session belongs to -- established by authenticate(), never guessed
    is_valid: bool  # => co-15: whether the credentials actually checked out -- False for a bad password


CREDENTIALS = {
    "alice": "correct-horse",
    "bob": "battery-staple",
}  # => co-15: a real, if tiny, password store
DOCUMENTS = {
    "doc-1": "alice",
    "doc-2": "bob",
}  # => co-16: a real ownership map -- document id -> owning user


def authenticate(
    user_id: str, password: str
) -> Session:  # => co-15: STEP 1 -- proves WHO is making the request
    expected = CREDENTIALS.get(
        user_id
    )  # => co-15: the real stored password for this user_id, or None
    is_valid = (
        expected is not None and expected == password
    )  # => co-15: a real, explicit credential comparison
    return Session(
        user_id=user_id, is_valid=is_valid
    )  # => co-15: identity established (or not) -- NOT permission


def authorize(
    session: Session, document_id: str
) -> bool:  # => co-15: STEP 2 -- decides WHAT the session may do
    if (
        not session.is_valid
    ):  # => co-15: an invalid (failed-authn) session is NEVER authorized for anything
        return False  # => co-15: short-circuits before even checking the resource -- authn is a precondition
    owner = DOCUMENTS.get(
        document_id
    )  # => co-16: the REAL owner of this specific resource, looked up server-side
    return (
        owner == session.user_id
    )  # => co-16: authorization is resource-SPECIFIC -- a separate question per call


def main() -> (
    None
):  # => co-15: runs three real scenarios through the SAME two separate functions
    print(
        "=== scenario 1: alice authenticates, reads her OWN document ==="
    )  # => labels section
    alice_session = authenticate(
        "alice", "correct-horse"
    )  # => co-15: a REAL authentication call, correct password
    print(
        f"authenticate() -> {alice_session}"
    )  # => co-15: real Session object -- is_valid=True
    print(
        f"authorize(doc-1) -> {authorize(alice_session, 'doc-1')}"
    )  # => co-16: real check -- alice OWNS doc-1
    assert alice_session.is_valid and authorize(
        alice_session, "doc-1"
    )  # => co-15/16: both checks pass, separately

    print(
        "\n=== scenario 2: alice authenticates, but is NOT authorized for bob's document ==="
    )  # => labels section
    print(
        f"authenticate() -> {alice_session}"
    )  # => co-15: SAME valid session -- authn already succeeded
    print(
        f"authorize(doc-2) -> {authorize(alice_session, 'doc-2')}"
    )  # => co-16: real check -- alice does NOT own doc-2
    assert alice_session.is_valid and not authorize(
        alice_session, "doc-2"
    )  # => co-15: authn true, co-16: authz false

    print(
        "\n=== scenario 3: a wrong password fails authn -- authz never even matters ==="
    )  # => labels section
    bad_session = authenticate(
        "alice", "wrong-password"
    )  # => co-15: a REAL authentication call, WRONG password
    print(
        f"authenticate() -> {bad_session}"
    )  # => co-15: real Session object -- is_valid=False this time
    print(
        f"authorize(doc-1) -> {authorize(bad_session, 'doc-1')}"
    )  # => co-16: real check -- short-circuits to False
    assert not bad_session.is_valid and not authorize(
        bad_session, "doc-1"
    )  # => co-15: authn false, co-16: authz false


if (
    __name__ == "__main__"
):  # => co-15: only runs when launched directly, e.g. `python3 authn_vs_authz.py`
    main()  # => co-15: runs all three real scenarios through authenticate() and authorize() separately
