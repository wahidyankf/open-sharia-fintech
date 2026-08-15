"""Example 34: minimal, fixed-algorithm JWT-style integrity demonstration."""

from __future__ import annotations  # => Supports the explicit return types below.

import base64  # => JWT parts use URL-safe base64 encoding.
import hashlib  # => SHA-256 feeds HMAC; it is not used as password storage.
import hmac  # => Constant-time comparison protects the verification result.
import json  # => Demonstration claims are serialized locally.

SECRET = b"demo-only-key-not-a-production-secret"  # => Fixed synthetic key is safe only for this teaching file.


def encoded(
    value: dict[str, str],
) -> str:  # => Converts a controlled JSON object to a JWT segment.
    raw = json.dumps(
        value, separators=(",", ":")
    ).encode()  # => Canonical compact bytes for this demo.
    return (
        base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
    )  # => JWT-compatible URL-safe text.


def issue(subject: str) -> str:  # => Produces an integrity-protected test token.
    header = encoded(
        {"alg": "HS256", "typ": "JWT"}
    )  # => Trusted policy fixes the accepted algorithm.
    payload = encoded(
        {"sub": subject}
    )  # => Subject is the only synthetic claim in this demonstration.
    signing_input = (
        header + "." + payload
    )  # => Header and payload are the exact signed input.
    signature = hmac.new(
        SECRET, signing_input.encode(), hashlib.sha256
    ).digest()  # => Server computes HMAC.
    return f"{signing_input}.{base64.urlsafe_b64encode(signature).rstrip(b'=').decode()}"  # => Three segments.


def accepts(token: str) -> bool:  # => Verifier treats token data as untrusted.
    header, payload, supplied = token.split(
        "."
    )  # => Malformed tokens intentionally raise in this small demo.
    if (
        json.loads(base64.urlsafe_b64decode(header + "=="))["alg"] != "HS256"
    ):  # => Never trust an arbitrary algorithm.
        return False  # => Reject downgrade or algorithm-confusion attempts.
    expected = hmac.new(
        SECRET, f"{header}.{payload}".encode(), hashlib.sha256
    ).digest()  # => Recompute signature.
    actual = base64.urlsafe_b64decode(
        supplied + "=="
    )  # => Decode supplied bytes before comparing.
    return hmac.compare_digest(expected, actual)  # => Constant-time integrity decision.


if __name__ == "__main__":  # => Safe local accept/reject demonstration.
    token = issue("learner-42")  # => Valid synthetic token.
    print(accepts(token))  # => Expected: True.
    print(accepts(token[:-2] + "aa"))  # => Expected: False after tampering.
