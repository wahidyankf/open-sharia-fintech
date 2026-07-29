# pyright: strict
"""Example 31: PKCE -- code_verifier / code_challenge. (co-16)

PKCE (RFC 7636) protects PUBLIC clients (SPAs, mobile apps) from
authorization-code interception: the client sends a derived code_challenge,
and redeems the code with the original code_verifier. The OAuth 2.0 Security
BCP (RFC 9700, Jan 2025) MANDATES PKCE for public clients. The challenge is
S256: base64url(sha256(verifier)).
"""

import base64  # => stdlib: base64url for the challenge
import hashlib  # => stdlib: SHA-256 to derive the challenge from the verifier


def make_verifier() -> str:  # => co-16: a high-entropy random string the client keeps secret
    # => In production this MUST be cryptographically random (e.g. secrets.token_urlsafe(48)).
    # => A fixed value is used here only so this example's captured output is reproducible.
    return "fixed-but-high-entropy-demo-verifier-3Kx9pQ2vWm7ZnR4t"  # => demo verifier (kept secret by the client)


def s256_challenge(verifier: str) -> str:  # => co-16: S256 = base64url(sha256(verifier)) with no padding
    digest = hashlib.sha256(verifier.encode("ascii")).digest()  # => the SHA-256 hash of the verifier
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")  # => base64url, no padding


def redeem(code: str, verifier: str, expected_challenge: str) -> str:  # => co-16: the token endpoint checks the verifier
    if s256_challenge(verifier) != expected_challenge:  # => the verifier does NOT derive to the stored challenge
        return "error: pkce verification failed"  # => an interceptor with the code but not the verifier is blocked
    return f"access-token-for-{code}"  # => success


verifier = make_verifier()  # => the client generates the verifier (kept secret in the app)
challenge = s256_challenge(verifier)  # => co-16: the challenge sent to the auth server with the auth request
print(f"verifier (kept secret): {verifier[:16]}...")  # => Output: a random prefix
print(f"challenge (S256, sent): {challenge[:24]}...")  # => Output: the derived challenge

ok = redeem("auth-code-xyz", verifier, challenge)  # => co-16: the RIGHT verifier -> success
print(f"correct verifier: {ok}")  # => Output: access-token-for-auth-code-xyz

attacker = redeem("auth-code-xyz", "a-different-wrong-verifier", challenge)  # => co-16: a WRONG verifier -> blocked
print(f"wrong verifier:   {attacker}")  # => Output: pkce verification failed

assert ok.startswith("access-token") and attacker.startswith("error")  # => co-16: only the real verifier redeems
