# pyright: strict
"""Example 55: Signing an Outbound Webhook Payload with HMAC. (co-33)

Since a webhook receiver cannot verify TLS-level origin the way a browser
does, the sender signs the payload with a SHARED SECRET (HMAC-SHA256); the
receiver recomputes the same signature to confirm the payload is genuine.
"""

import hashlib  # => stdlib: the underlying hash function HMAC is built on
import hmac  # => stdlib: computes and verifies the HMAC signature itself

SHARED_SECRET = b"webhook-shared-secret-key"  # => co-33: known to BOTH sender and receiver, never sent


def sign_payload(payload: bytes, secret: bytes) -> str:  # => co-33: the SENDER's own signing step
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()  # => co-33: HMAC-SHA256 over the payload


def verify_signature(payload: bytes, signature: str, secret: bytes) -> bool:  # => co-33: the RECEIVER's check
    expected = sign_payload(payload, secret)  # => co-33: recomputes the SAME signature independently
    return hmac.compare_digest(expected, signature)  # => co-33: constant-time comparison, timing-attack-safe


event_payload = b'{"event": "article.created", "id": 1}'  # => the outbound webhook's own JSON body
signature = sign_payload(event_payload, SHARED_SECRET)  # => co-33: the SENDER signs it before delivery
print(f"X-Webhook-Signature: {signature}")  # => Output: a 64-char hex digest

genuine = verify_signature(event_payload, signature, SHARED_SECRET)  # => the RECEIVER checks a genuine payload
print(f"genuine payload verifies: {genuine}")  # => Output: True -- co-33: signatures match

tampered_payload = b'{"event": "article.created", "id": 999}'  # => an ATTACKER-modified payload
tampered_check = verify_signature(tampered_payload, signature, SHARED_SECRET)  # => co-33: checked against OLD sig
# => tampered_check is False -- the old signature no longer matches the new payload's own hash
print(f"tampered payload verifies: {tampered_check}")  # => Output: False -- co-33: signature no longer matches
