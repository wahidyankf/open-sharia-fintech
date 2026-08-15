"""Capstone mechanism proof: valid inputs pass; altered inputs fail locally."""

from __future__ import (
    annotations,
)  # => Keeps annotations consistent with the course examples.

import base64  # => Encodes the compact token signature safely for URL transport.
import hashlib  # => Supplies SHA-256 to the HMAC construction below.
import hmac  # => Verifies token integrity with a constant-time comparison.

from argon2 import (
    PasswordHasher,
)  # => Uses Argon2id rather than a fast general-purpose hash.
from argon2.exceptions import (
    VerifyMismatchError,
)  # => Wrong credentials are an expected rejection.
from cryptography.exceptions import (
    InvalidSignature,
)  # => Changed signed bytes must be rejected.
from cryptography.hazmat.primitives.asymmetric import (
    ed25519,
)  # => Maintained signature implementation.

HASHER = PasswordHasher(
    memory_cost=19_456, time_cost=2, parallelism=1
)  # => OWASP minimum-tier baseline.
TOKEN_KEY = b"capstone-demo-key-only-not-a-deployed-secret"  # => Synthetic key stays inside this local proof.


def password_is_valid(
    candidate: str,
) -> bool:  # => Accepts a candidate without storing plaintext.
    stored = HASHER.hash(
        "capstone-password"
    )  # => Salt and parameters are encoded in the generated hash.
    try:  # => A wrong candidate takes the ordinary rejection branch.
        return HASHER.verify(
            stored, candidate
        )  # => Argon2id checks candidate against stored evidence.
    except VerifyMismatchError:  # => Expected invalid-password result.
        return False  # => Fails closed with no detail leak.


def token_is_valid(
    token: str,
) -> bool:  # => Token format is `payload.signature` for this narrow proof.
    payload, supplied = token.split(
        ".", 1
    )  # => Separates untrusted payload from its claimed signature.
    expected = hmac.new(
        TOKEN_KEY, payload.encode(), hashlib.sha256
    ).digest()  # => Computes server-side integrity evidence.
    actual = base64.urlsafe_b64decode(
        supplied + "=="
    )  # => Decodes supplied signature bytes.
    return hmac.compare_digest(
        expected, actual
    )  # => Constant-time equality protects the decision.


def signature_is_valid(
    message: bytes,
) -> bool:  # => Tests a changed message against an original signature.
    private_key = (
        ed25519.Ed25519PrivateKey.generate()
    )  # => Fresh key exists only during this process.
    signature = private_key.sign(
        message
    )  # => Original bytes receive a private-key signature.
    try:  # => Altered bytes should trigger the deliberate rejection path.
        private_key.public_key().verify(
            signature, message + b" changed"
        )  # => Tampering invalidates the signature.
    except InvalidSignature:  # => Library proves integrity failure.
        return False  # => Rejects tampering.
    return True  # => Would indicate an unexpected verification failure.


if __name__ == "__main__":  # => Executes three local accept/reject assertions.
    payload = "learner-42"  # => Synthetic subject with no personal data.
    signature = hmac.new(
        TOKEN_KEY, payload.encode(), hashlib.sha256
    ).digest()  # => Produces a valid local signature.
    valid_token = (
        payload + "." + base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
    )  # => Builds test token.
    assert password_is_valid("capstone-password")  # => Correct password is accepted.
    assert not password_is_valid("wrong")  # => Wrong password is rejected.
    assert token_is_valid(valid_token)  # => Original token is accepted.
    assert not token_is_valid(valid_token[:-2] + "aa")  # => Altered token is rejected.
    assert not signature_is_valid(
        b"approve invoice"
    )  # => Altered signed message is rejected.
    print("capstone security mechanisms: pass")  # => Clear local completion signal.
