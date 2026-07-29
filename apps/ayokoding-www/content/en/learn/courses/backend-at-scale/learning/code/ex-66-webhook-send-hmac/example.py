# pyright: strict
"""Example 66: Webhook -- send with an HMAC-SHA256 signature. (co-32)

An outbound webhook is signed with HMAC-SHA256 over the payload using a
shared secret, so the receiver can prove the payload came from a party that
knows the secret (authentication layered on top of HTTPS transport security).
This example models Stripe's `Stripe-Signature` header shape.
"""

import hashlib  # => stdlib: SHA-256 for the HMAC
import hmac  # => stdlib: HMAC-SHA256 computation
import json  # => stdlib: serialize the payload to bytes

SECRET = b"whsec-shared-secret"  # => the shared secret (in production, loaded from env)


def sign(timestamp: str, payload: bytes) -> str:  # => co-32: Stripe-style signature
    signed_payload = f"{timestamp}.".encode() + payload  # => t=<ts> + "." + payload
    digest = hmac.new(SECRET, signed_payload, hashlib.sha256).hexdigest()  # => HMAC-SHA256
    return f"t={timestamp},v1={digest}"  # => co-32: the Stripe-Signature header value


def send_webhook(event: dict[str, str]) -> tuple[bytes, str]:  # => returns (payload bytes, signature header)
    payload = json.dumps(event).encode()  # => the canonical payload bytes
    timestamp = "1700000000"  # => a fixed timestamp for this demo (Stripe includes a real ts for replay protection)
    signature = sign(timestamp, payload)  # => co-32: sign over timestamp.payload
    return payload, signature  # => the POST body + the Stripe-Signature header


payload, signature = send_webhook({"event": "order.shipped", "order_id": "42"})  # => send one webhook
print(f"payload: {payload.decode()}")  # => Output: the JSON body
print(f"Stripe-Signature: {signature[:48]}...")  # => Output: a prefix of the header (t=...,v1=...)

# Recompute independently to prove the signature matches the payload (a receiver would do this).
ts = signature.split(",")[0].split("=")[1]  # => extract the timestamp
expected = sign(ts, payload)  # => co-32: recompute over the SAME timestamp.payload
matches = hmac.compare_digest(expected, signature)  # => constant-time compare
print(f"signature matches payload: {matches}")  # => Output: True

assert matches is True  # => co-32: the signature verifies against the payload it covers
