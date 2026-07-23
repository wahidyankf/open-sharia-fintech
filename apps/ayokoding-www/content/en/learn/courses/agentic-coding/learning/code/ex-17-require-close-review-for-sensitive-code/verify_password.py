# learning/code/ex-17-require-close-review-for-sensitive-code/verify_password.py
"""Example ex-17: Require Close Review for Sensitive Code -- Password-Hash Check."""  # => co-17: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import hashlib  # => co-17: hashlib.pbkdf2_hmac -- the KDF this example hashes passwords with
import hmac  # => co-17: hmac.compare_digest -- constant-time comparison, the line-by-line review's #1 concern

ITERATIONS = 200_000  # => co-17: PBKDF2 iteration count -- reviewed for being high enough to resist brute force


def hash_password(password: str, salt: bytes) -> bytes:  # => co-17: the KDF step -- reviewed line 1 of the checklist below
    """Derive a PBKDF2-HMAC-SHA256 hash of `password` salted with `salt`."""  # => co-17: documents hash_password's contract
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)  # => co-17: stdlib KDF, no custom crypto


# --- LINE-BY-LINE REVIEW CHECKLIST (co-17) -- completed BEFORE acceptance ----  # => co-17: the review this sensitive diff required
# [x] uses a real KDF (pbkdf2_hmac), not a bare hash -- resists brute force      # => co-17: checklist item 1, checked
# [x] iteration count (200_000) meets a documented minimum for PBKDF2-SHA256     # => co-17: checklist item 2, checked
# [x] comparison uses hmac.compare_digest, NEVER `==` -- avoids timing attacks   # => co-17: checklist item 3, checked
# [x] salt is a parameter, never hardcoded or reused across users                # => co-17: checklist item 4, checked
# ------------------------------------------------------------------------------  # => co-17: closes the checklist block
def verify_password(stored_hash: bytes, password: str, salt: bytes) -> bool:  # => co-17: THE diff under close review -- reviewed line by line above
    """Check `password` against `stored_hash`, in constant time."""  # => co-17: documents verify_password's contract
    candidate = hash_password(password, salt)  # => co-17: re-derive the hash from the CANDIDATE password, using the same salt
    return hmac.compare_digest(candidate, stored_hash)  # => co-17: constant-time compare -- checklist item 3, enforced in code


if __name__ == "__main__":  # => co-17: entry point -- this block runs only when the file executes directly, not on import
    salt = b"fixed-demo-salt-do-not-reuse"  # => co-17: a FIXED salt only for this reproducible demo -- production code generates one per user
    stored = hash_password("correct horse battery staple", salt)  # => co-17: the "stored" hash, as it would live in a user record
    right = verify_password(stored, "correct horse battery staple", salt)  # => co-17: the correct password
    wrong = verify_password(stored, "wrong password", salt)  # => co-17: an incorrect password
    print(f"verify_password(correct password) = {right}")  # => co-17: expect True
    print(f"verify_password(wrong password)   = {wrong}")  # => co-17: expect False
    assert right is True, "the correct password must verify"  # => co-17: confirms the happy path
    assert wrong is False, "an incorrect password must NOT verify"  # => co-17: confirms rejection works
    print("Checklist item 3 in effect: comparison never used == on secret bytes: True")  # => co-17: reached only if both asserts above passed
