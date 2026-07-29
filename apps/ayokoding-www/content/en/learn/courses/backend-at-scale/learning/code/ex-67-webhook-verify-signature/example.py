# pyright: strict
"""Example 67: Webhook -- verify an incoming signature. (co-32)

The receiver recomputes the HMAC over the received timestamp.payload and
compares it to the header's signature in CONSTANT TIME (hmac.compare_digest).
A tampered body produces a different digest -> rejected. Source: GitHub
X-Hub-Signature-256 validating deliveries (HMAC-SHA256, constant-time).
"""

import hashlib  # => stdlib: SHA-256 for the HMAC
import hmac  # => stdlib: HMAC-SHA256 + constant-time compare

SECRET = b"whsec-shared-secret"  # => the shared secret the sender and receiver share
TOLERANCE_SECONDS = 300  # => reject signatures older than this (replay protection), via a fixed clock here


def sign(timestamp: str, payload: bytes) -> str:  # => the sender's signature function (reused)
    signed = f"{timestamp}.".encode() + payload  # => timestamp.payload
    return hmac.new(SECRET, signed, hashlib.sha256).hexdigest()  # => the v1 digest


def verify(timestamp: str, payload: bytes, v1: str) -> bool:  # => co-32: the receiver's verification
    expected = sign(timestamp, payload)  # => recompute over the received timestamp.payload
    return hmac.compare_digest(expected, v1)  # => co-32: CONSTANT-TIME compare (avoids timing oracles)


payload = b'{"event":"order.shipped"}'  # => a genuine payload
timestamp = "1700000000"  # => the sender's timestamp
good_signature = sign(timestamp, payload)  # => the legitimate signature

valid = verify(timestamp, payload, good_signature)  # => co-32: matches -> accepted
print(f"genuine payload verifies: {valid}")  # => Output: True

tampered = verify(timestamp, b'{"event":"order.CANCELLED"}', good_signature)  # => co-32: body changed -> digest differs
print(f"tampered body verifies:   {tampered}")  # => Output: False -- rejected

bogus_sig = verify(timestamp, payload, "0" * 64)  # => a forged signature -> rejected
print(f"forged signature verifies: {bogus_sig}")  # => Output: False

assert valid is True and tampered is False and bogus_sig is False  # => co-32: only the genuine body+signature passes
