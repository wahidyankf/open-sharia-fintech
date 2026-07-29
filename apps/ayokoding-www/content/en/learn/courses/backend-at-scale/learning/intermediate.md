---
title: "Intermediate Examples"
date: 2026-07-29T00:00:00+07:00
draft: false
weight: 20
---

Examples 29-56 cover auth, limits, caches, and observability: the OAuth2 authorization-code flow and OIDC id_token, PKCE, refresh-token rotation and reuse detection, the four rate-limit algorithms (token bucket, leaky bucket, fixed window's boundary-burst flaw, sliding window) and 429 + Retry-After, cache-aside and write-through, TTL expiry and explicit invalidation (and the stale-data bug a wrong TTL causes), HTTP caching with ETag/If-None-Match and Cache-Control, OpenTelemetry spans and W3C traceparent propagation, liveness vs readiness probes, GraphQL field selection and the N+1 resolver fixed by DataLoader batching, gRPC unary and server-streaming RPCs, and a REST/GraphQL/gRPC contrast. Every example is complete, self-contained, originally-authored standard-library Python. Run each with `python3 example.py`; every printed line below is a real captured run.

---

### Example 29: OAuth 2.0 Authorization Code Flow

_ex-29 &middot; exercises co-15_

Model the authorization-code grant: the client redirects to the auth server, which returns a short-lived CODE; the client exchanges that code (plus its secret) at the token endpoint for an access token (RFC 6749).

**`learning/code/ex-29-oauth2-authcode-flow/example.py`**

```python
# pyright: strict
"""Example 29: OAuth 2.0 Authorization Code flow. (co-15)

Model the authorization-code grant in-process: the client redirects to the
auth server, which returns a short-lived CODE; the client exchanges that
code (plus its secret) at the token endpoint for an access token. OAuth 2.0
GRANTS AUTHORIZATION (can you do this?), not authentication. Source: RFC 6749.
"""

from dataclasses import dataclass  # => a small typed record for the token response


@dataclass  # => co-15: the token endpoint's response
class TokenResponse:
    access_token: str  # => the bearer token the client uses against protected resources
    token_type: str  # => always "Bearer" here
    expires_in: int  # => the access token's lifetime in seconds


# A toy auth server: one authorization code, bound to one client + its secret.
AUTH_CODE = "auth-code-abc"  # => the short-lived code the auth server issued
CODE_TO_CLIENT = {AUTH_CODE: ("client-7", "client-secret")}  # => code -> (client_id, client_secret)


def exchange_code(code: str, client_id: str, client_secret: str) -> TokenResponse | str:
    # => co-15: the token endpoint -- exchange a code for an access token
    record = CODE_TO_CLIENT.get(code)  # => look up the code
    if record is None:  # => unknown code -> denied
        return "invalid_grant: unknown code"  # => error
    expected_client, expected_secret = record  # => the client + secret bound to THIS code
    if client_id != expected_client or client_secret != expected_secret:  # => client credentials mismatch
        return "invalid_client: credentials do not match"  # => error
    return TokenResponse(access_token=f"access-{client_id}", token_type="Bearer", expires_in=3600)  # => success


good = exchange_code(AUTH_CODE, "client-7", "client-secret")  # => co-15: correct code + credentials
print(f"valid exchange: {good}")  # => Output: TokenResponse(access-token='access-client-7', ...)

wrong_secret = exchange_code(AUTH_CODE, "client-7", "wrong")  # => wrong secret -> rejected
print(f"wrong secret:   {wrong_secret}")  # => Output: invalid_client error

unknown = exchange_code("bogus-code", "client-7", "client-secret")  # => unknown code -> rejected
print(f"unknown code:   {unknown}")  # => Output: invalid_grant error

assert isinstance(good, TokenResponse) and good.token_type == "Bearer"  # => co-15: code exchanges for a token
assert not isinstance(wrong_secret, TokenResponse)  # => wrong credentials are rejected
```

**Run**: `python3 example.py`

**Output**:

```text
valid exchange: TokenResponse(access_token='access-client-7', token_type='Bearer', expires_in=3600)
wrong secret:   invalid_client: credentials do not match
unknown code:   invalid_grant: unknown code
```

**Key takeaway**: OAuth2's auth-code flow exchanges a short-lived code for an access token -- it GRANTS authorization, not authentication.

**Why it matters**: OAuth 2.0 grants authorization (what you may do); OIDC adds authentication (who you are) -- Example 30.

---

### Example 30: OpenID Connect -- an id_token Carries Identity

_ex-30 &middot; exercises co-15_

OpenID Connect is an IDENTITY LAYER on top of OAuth 2.0: alongside the access token, the token endpoint also issues an id_token -- a JWT whose claims (sub, email) describe WHO the user is.

**`learning/code/ex-30-oidc-id-token/example.py`**

```python
# pyright: strict
"""Example 30: OpenID Connect -- an id_token carries identity. (co-15)

OpenID Connect (OIDC) is an IDENTITY LAYER on top of OAuth 2.0: alongside
the access token, the token endpoint also issues an id_token -- a JWT whose
claims (sub, email) describe WHO the user is. So OAuth 2.0 = authorization,
OIDC = authentication. Source: OpenID Connect Core 1.0.
"""

import base64  # => stdlib: base64url for the JWT segments
import hashlib  # => stdlib: SHA-256 for HMAC
import hmac  # => stdlib: HMAC-SHA256 signing
import json  # => stdlib: serialize header and claims

SECRET = b"oidc-secret"  # => the HMAC shared secret


def b64url(raw: bytes) -> str:  # => base64url without padding
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")  # => JWT segment format


def sign(message: bytes) -> str:  # => HMAC-SHA256 -> base64url
    return b64url(hmac.new(SECRET, message, hashlib.sha256).digest())  # => keyed hash


def issue_id_token(subject: str, email: str) -> str:  # => co-15: the id_token is a SIGNED JWT
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())  # => header segment
    claims: dict[str, object] = {"sub": subject, "email": email, "iss": "https://idp.example.com"}  # => identity claims
    payload = b64url(json.dumps(claims, separators=(",", ":")).encode())  # => claims segment
    return f"{header}.{payload}.{sign(f'{header}.{payload}'.encode())}"  # => the signed id_token


def decode_id_token(token: str) -> dict[str, object]:  # => verify + decode the id_token's claims
    _header, payload_b64, signature = token.split(".")  # => the three segments
    assert hmac.compare_digest(sign(token.rsplit(".", 1)[0].encode()), signature)  # => signature valid
    return json.loads(base64.urlsafe_b64decode(payload_b64 + "=="))  # => the verified identity claims


# The token endpoint returns BOTH an access_token (OAuth2 -- what you may do) and an id_token (OIDC -- who you are).
access_token = "access-for-user-42"  # => co-15: OAuth2 -- authorization
id_token = issue_id_token(subject="user-42", email="ada@example.com")  # => co-15: OIDC -- authentication
print(f"token endpoint returned access_token + id_token (truncated): {access_token}, {id_token[:24]}...")

identity = decode_id_token(id_token)  # => co-15: the id_token's claims describe the user
print(f"verified identity (sub): {identity['sub']}, email: {identity['email']}")  # => Output: user-42, ada@example.com

assert identity["sub"] == "user-42" and identity["email"] == "ada@example.com"  # => co-15: OIDC carries identity
```

**Run**: `python3 example.py`

**Output**:

```text
token endpoint returned access_token + id_token (truncated): access-for-user-42, eyJhbGciOiJIUzI1NiIsInR5...
verified identity (sub): user-42, email: ada@example.com
```

**Key takeaway**: OIDC's id_token is a signed JWT carrying identity claims (sub) -- authentication on top of OAuth2's authorization.

**Why it matters**: Conflating OAuth2 and OIDC is a classic security mistake; they answer different questions.

---

### Example 31: PKCE -- code_verifier / code_challenge

_ex-31 &middot; exercises co-16_

PKCE (RFC 7636) protects PUBLIC clients from authorization-code interception: the client sends a derived code_challenge and redeems the code with the original code_verifier. The OAuth security BCP (RFC 9700) MANDATES PKCE for public clients.

**`learning/code/ex-31-pkce-challenge/example.py`**

```python
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
```

**Run**: `python3 example.py`

**Output**:

```text
verifier (kept secret): fixed-but-high-e...
challenge (S256, sent): nAz6k-tm-KJnuZStfrKO8Kio...
correct verifier: access-token-for-auth-code-xyz
wrong verifier:   error: pkce verification failed
```

**Key takeaway**: PKCE derives the challenge from a secret verifier; an interceptor with the code but not the verifier is blocked.

**Why it matters**: PKCE closes the auth-code interception attack for SPAs and mobile apps that cannot hold a client secret.

---

### Example 32: Refresh-Token Rotation

_ex-32 &middot; exercises co-18_

Short-lived access tokens limit a stolen token's lifetime; a long-lived refresh token lets a client get a NEW access token without re-authenticating. ROTATION issues a NEW refresh token on every use, so each is single-use.

**`learning/code/ex-32-refresh-rotate/example.py`**

```python
# pyright: strict
"""Example 32: Refresh-token rotation. (co-18)

Short-lived access tokens limit a stolen token's lifetime; a long-lived
refresh token lets a client get a NEW access token without re-authenticating.
ROTATION issues a NEW refresh token on every use, so each refresh token is
single-use. NOTE: RFC 9700 Sec 2.2.2 requires public-client refresh tokens to
be "sender-constrained OR use rotation" -- one of two mitigations, not an
unconditional mandate.
"""

from dataclasses import dataclass  # => a small typed record for the issued pair


@dataclass(frozen=True)  # => co-18: the pair a refresh issues: a new access token + a NEW rotated refresh
class TokenPair:
    access_token: str  # => short-lived bearer token
    refresh_token: str  # => the NEW refresh token (the old one is now invalid)


# The store of CURRENTLY-valid refresh tokens. Rotation removes the used one and adds the new one.
VALID_REFRESH: set[str] = {"refresh-0"}  # => the initial refresh token issued at sign-in
ISSUE_COUNTER = [1]  # => a counter to mint distinct new tokens deterministically


def rotate(presented_refresh: str) -> TokenPair | None:  # => co-18: exchange a refresh for a new pair
    if presented_refresh not in VALID_REFRESH:  # => the presented refresh is not (or no longer) valid
        return None  # => rejected
    VALID_REFRESH.remove(presented_refresh)  # => co-18: rotation -- the used refresh is now INVALID
    new_refresh = f"refresh-{ISSUE_COUNTER[0]}"  # => mint a NEW single-use refresh token
    ISSUE_COUNTER[0] += 1  # => advance the counter
    VALID_REFRESH.add(new_refresh)  # => the new refresh is now the only valid one
    return TokenPair(access_token=f"access-{ISSUE_COUNTER[0]}", refresh_token=new_refresh)  # => the new pair


first = rotate("refresh-0")  # => co-18: the initial refresh -> a new access + rotated refresh
assert first is not None  # => type-narrow for pyright
print(f"first rotation:  access={first.access_token}, refresh={first.refresh_token}")  # => Output: new pair

second = rotate(first.refresh_token)  # => co-18: the rotated refresh -> ANOTHER new pair
assert second is not None  # => type-narrow
print(f"second rotation: access={second.access_token}, refresh={second.refresh_token}")  # => Output: another new pair

reused = rotate(first.refresh_token)  # => co-18: the OLD (already-rotated) refresh -> REJECTED
print(f"reused old refresh: {reused}")  # => Output: None -- single-use, rotation invalidated it

assert second.refresh_token != first.refresh_token  # => co-18: each rotation mints a distinct refresh
assert reused is None  # => co-18: an already-used refresh is no longer valid
```

**Run**: `python3 example.py`

**Output**:

```text
first rotation:  access=access-2, refresh=refresh-1
second rotation: access=access-3, refresh=refresh-2
reused old refresh: None
```

**Key takeaway**: Rotation mints a NEW refresh token on every use -- the old one is immediately invalid.

**Why it matters**: RFC 9700 Sec 2.2.2 requires public-client refresh tokens to be sender-constrained OR rotated -- one of two mitigations, not an unconditional mandate.

---

### Example 33: Refresh-Token Reuse Detection

_ex-33 &middot; exercises co-18_

If a refresh token that was ALREADY rotated out is presented again, an attacker stole the original. Detection REVOKES the entire token family, invalidating every token derived from the original sign-in.

**`learning/code/ex-33-refresh-reuse-detect/example.py`**

```python
# pyright: strict
"""Example 33: Refresh-token reuse detection. (co-18)

If a refresh token that was ALREADY rotated out is presented again, that
means an attacker stole the original and is trying to use it after the
legitimate client already rotated. Detection REVOKESS the entire token
family, invalidating every token derived from the original sign-in.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-18: tracks a token family so reuse can revoke the whole chain
class RefreshStore:
    active: set[str] = field(default_factory=lambda: {"r-0"})  # => currently-valid refresh tokens
    used: set[str] = field(default_factory=set[str])  # => refresh tokens already rotated OUT
    revoked: bool = False  # => whether the family has been burned by a detected reuse
    counter: list[int] = field(default_factory=lambda: [1])  # => a mutable counter cell


def rotate(store: RefreshStore, presented: str) -> str | None:  # => co-18: rotate, OR detect reuse + revoke
    if store.revoked:  # => the family was already burned by a prior reuse detection
        return None  # => nothing issues anymore
    if presented in store.used:  # => co-18: a USED-then-rotated token reappears -> REUSE DETECTED
        store.active.clear()  # => revoke the ENTIRE family -- every active token is now invalid
        store.revoked = True  # => mark the family burned so all future calls short-circuit
        return None  # => signal: reuse detected, family revoked
    if presented not in store.active:  # => a refresh that was never valid in this family
        return None  # => rejected
    store.active.remove(presented)  # => the used token leaves the active set
    store.used.add(presented)  # => ...and lands in the used set, so a replay triggers detection
    new_token = f"r-{store.counter[0]}"  # => mint the next token in the family
    store.counter[0] += 1  # => advance
    store.active.add(new_token)  # => the new token is now the active one
    return new_token  # => the rotated refresh


store = RefreshStore()  # => co-18: one family's state

first = rotate(store, "r-0")  # => co-18: legitimate rotation -> new active token
assert first is not None  # => type-narrow
print(f"legitimate rotation: {first}")  # => Output: r-1

attacker_replay = rotate(store, "r-0")  # => co-18: the STOLEN, already-used token -> REUSE DETECTED
print(f"attacker replays stolen r-0: {attacker_replay} (family revoked)")  # => Output: None

legit_after_breach = rotate(store, first)  # => co-18: even the legitimate new token is now revoked
print(f"legitimate client uses r-1 after breach: {legit_after_breach}")  # => Output: None -- family burned

assert attacker_replay is None and legit_after_breach is None  # => co-18: reuse revoked the whole family
assert store.revoked and len(store.active) == 0  # => co-18: no active token survives a detected reuse
```

**Run**: `python3 example.py`

**Output**:

```text
legitimate rotation: r-1
attacker replays stolen r-0: None (family revoked)
legitimate client uses r-1 after breach: None
```

**Key takeaway**: A replayed, already-rotated refresh token signals theft -- the whole family is revoked.

**Why it matters**: Reuse detection turns a stolen refresh token from a silent breach into a loud, self-healing one.

---

### Example 34: Token-Bucket Rate Limiter

_ex-34 &middot; exercises co-19_

A token bucket holds up to `capacity` tokens and refills at `rate` per second; each call consumes one. It ALLOWS BURSTS up to capacity, then throttles to the refill rate (AWS API Gateway uses it).

**`learning/code/ex-34-token-bucket/example.py`**

```python
# pyright: strict
"""Example 34: Token-bucket rate limiter. (co-19)

A token bucket holds up to `capacity` tokens and refills at `rate` per
second; each call consumes one token. It ALLOWS BURSTS up to capacity (a
client may spend a full bucket at once), then throttles to the refill rate.
AWS API Gateway uses this algorithm. The clock is INJECTED so output is
deterministic.
"""

from dataclasses import dataclass  # => a small typed record for the limiter's state


@dataclass  # => co-19: the bucket's mutable state
class TokenBucket:
    capacity: int  # => the max tokens the bucket can hold (burst size)
    rate: float  # => tokens added per second (steady-state throughput)
    tokens: float  # => current token count
    last_refill: float  # => the (injected) clock time of the last refill computation


def refill(bucket: TokenBucket, now: float) -> None:  # => co-19: add tokens elapsed since the last refill
    elapsed = now - bucket.last_refill  # => seconds passed since the last refill
    bucket.tokens = min(bucket.capacity, bucket.tokens + elapsed * bucket.rate)  # => refill, capped at capacity
    bucket.last_refill = now  # => advance the refill timestamp


def allow(bucket: TokenBucket, now: float) -> bool:  # => co-19: consume one token if available
    refill(bucket, now)  # => top up the bucket for elapsed time first
    if bucket.tokens >= 1.0:  # => enough tokens -> consume one
        bucket.tokens -= 1.0  # => consume
        return True  # => allowed
    return False  # => empty bucket -> denied (throttled)


bucket = TokenBucket(capacity=5, rate=1.0, tokens=5.0, last_refill=0.0)  # => co-19: 5-token burst, refills 1/sec

# t=0: a burst of 5 calls empties the bucket.
burst = [allow(bucket, now=0.0) for _ in range(5)]  # => all 5 succeed (capacity allows the burst)
print(f"burst of 5 at t=0: allowed={sum(burst)}")  # => Output: 5

denied = allow(bucket, now=0.0)  # => bucket empty at t=0 -> denied
print(f"6th call at t=0: {denied}")  # => Output: False -- throttled

# t=3: 3 seconds elapsed -> ~3 tokens refilled.
refilled = allow(bucket, now=3.0)  # => ~3 tokens available after refill -> allowed
print(f"call at t=3 (after refill): {refilled}")  # => Output: True -- tokens refilled over time

assert sum(burst) == 5 and denied is False and refilled is True  # => co-19: bursts allowed, then refill over time
```

**Run**: `python3 example.py`

**Output**:

```text
burst of 5 at t=0: allowed=5
6th call at t=0: False
call at t=3 (after refill): True
```

**Key takeaway**: A token bucket allows a burst up to capacity, then throttles to the refill rate -- tokens refill over time.

**Why it matters**: Burst-tolerance is the token bucket's defining property vs the leaky bucket's smoothing.

---

### Example 35: Leaky-Bucket Rate Limiter

_ex-35 &middot; exercises co-19_

A leaky bucket holds requests in a queue that DRAINS at a constant rate, smoothing bursts into a steady output stream.

**`learning/code/ex-35-leaky-bucket/example.py`**

```python
# pyright: strict
"""Example 35: Leaky-bucket rate limiter. (co-19)

A leaky bucket holds requests in a queue that DRAINS at a constant rate,
smoothing bursts into a steady output stream. A burst arrives all at once
but is spaced out to the drain rate. The clock is INJECTED for determinism.
"""

from dataclasses import dataclass  # => a small typed record for the limiter's state


@dataclass  # => co-19: the bucket's mutable state
class LeakyBucket:
    drain_rate: float  # => requests drained (processed) per second -- the smoothed output rate
    queue: list[float]  # => arrival timestamps of queued requests
    capacity: int  # => max queued requests before new arrivals are rejected
    last_drain: float  # => the (injected) clock time of the last drain computation


def drain(bucket: LeakyBucket, now: float) -> None:  # => co-19: remove requests that have "drained out" by now
    elapsed = now - bucket.last_drain  # => seconds passed since the last drain
    processed = int(elapsed * bucket.drain_rate)  # => how many requests drained in that window
    bucket.queue = bucket.queue[processed:]  # => drop the drained requests from the front
    bucket.last_drain = now  # => advance the drain timestamp


def admit(bucket: LeakyBucket, now: float) -> bool:  # => co-19: enqueue a request if room remains
    drain(bucket, now)  # => first drain whatever elapsed
    if len(bucket.queue) >= bucket.capacity:  # => queue full -> reject (backpressure)
        return False  # => denied
    bucket.queue.append(now)  # => enqueue this request's arrival
    return True  # => admitted (will be smoothed out at drain_rate)


bucket = LeakyBucket(drain_rate=2.0, queue=[], capacity=3, last_drain=0.0)  # => co-19: drains 2/sec, holds 3

# t=0: a burst of 5 arrives; only 3 fit the capacity, 2 are rejected.
results = [admit(bucket, now=0.0) for _ in range(5)]  # => 3 admitted, 2 rejected
print(f"burst of 5 at t=0: admitted={sum(results)}, rejected={5 - sum(results)}")  # => Output: 3, 2

# t=1: 1 second elapsed -> 2 requests drained out, making room for ~2 new.
after_drain = admit(bucket, now=1.0)  # => co-19: room freed by the constant drain -> admitted
print(f"call at t=1 (after drain): {after_drain}")  # => Output: True -- smoothed output makes room

assert sum(results) == 3 and after_drain is True  # => co-19: bursts smoothed to the drain rate over time
```

**Run**: `python3 example.py`

**Output**:

```text
burst of 5 at t=0: admitted=3, rejected=2
call at t=1 (after drain): True
```

**Key takeaway**: A leaky bucket smooths bursts into a constant drain rate -- the queue absorbs the spike.

**Why it matters**: Smoothing (leaky) vs burst-allowing (token) is the core rate-limit algorithm trade-off.

---

### Example 36: Fixed-Window Counter -- the Boundary-Burst Flaw

_ex-36 &middot; exercises co-19_

A fixed-window counter resets at each window boundary. The flaw: a caller can spend the FULL limit at the end of one window AND the full limit at the start of the next -- 2x the configured limit in a short span.

**`learning/code/ex-36-fixed-window/example.py`**

```python
# pyright: strict
"""Example 36: Fixed-window counter -- the boundary-burst flaw. (co-19)

A fixed-window counter resets at each window boundary (e.g. every 60s). The
flaw: a caller can spend the FULL limit at the end of one window AND the full
limit at the start of the next -- 2x the configured limit in a short span
straddling the boundary.
"""

from dataclasses import dataclass  # => a small typed record for the limiter's state


@dataclass  # => co-19: counts calls within the CURRENT fixed window
class FixedWindow:
    limit: int  # => max calls allowed PER window
    window_seconds: int  # => the window length
    count: int  # => calls so far in the current window
    window_start: int  # => the (injected) clock time at which the current window began


def allow(fw: FixedWindow, now: int) -> bool:  # => co-19: count one call, resetting on a window boundary
    if now >= fw.window_start + fw.window_seconds:  # => crossed into a NEW window -> reset the counter
        fw.window_start = now  # => the new window begins now
        fw.count = 0  # => reset
    if fw.count >= fw.limit:  # => this window is exhausted
        return False  # => denied
    fw.count += 1  # => count the call
    return True  # => allowed


fw = FixedWindow(limit=10, window_seconds=60, count=0, window_start=0)  # => co-19: 10 calls per 60s window

# t=58: spend the WHOLE limit at the tail end of window [0,60).
tail = sum(1 for _ in range(10) if allow(fw, now=58))  # => all 10 allowed in window 0
print(f"window 0, 10 calls at t=58: allowed={tail}")  # => Output: 10

eleventh = allow(fw, now=58)  # => window 0 exhausted -> denied
print(f"11th call still in window 0: {eleventh}")  # => Output: False

# t=60: a NEW window begins immediately -> the counter resets -> another 10 allowed.
head = sum(1 for _ in range(10) if allow(fw, now=60))  # => co-19: 10 MORE allowed at the start of window 1
print(f"window 1, 10 calls at t=60: allowed={head}")  # => Output: 10 -- the boundary burst

# In the 2-second span t=[58,60) the caller got 20 calls -- 2x the configured limit. That is the flaw.
boundary_burst = tail + head  # => co-19: 20 calls in ~2 seconds despite limit=10/window
print(f"calls in the 2s boundary span t=[58,60): {boundary_burst} (2x the limit)")  # => Output: 20

assert boundary_burst == 20 and eleventh is False  # => co-19: fixed window suffers 2x at the boundary
```

**Run**: `python3 example.py`

**Output**:

```text
window 0, 10 calls at t=58: allowed=10
11th call still in window 0: False
window 1, 10 calls at t=60: allowed=10
calls in the 2s boundary span t=[58,60): 20 (2x the limit)
```

**Key takeaway**: A fixed window lets a caller spend 2x the limit across a boundary -- the boundary-burst flaw.

**Why it matters**: This flaw is exactly what the sliding window (Example 37) avoids.

---

### Example 37: Sliding-Window Rate Limiter -- No Boundary Burst

_ex-37 &middot; exercises co-19_

A sliding window counts requests in a TRAILING window ending at NOW, so a burst straddling a former boundary is still bounded (no 2x flaw). Cloudflare uses this in production.

**`learning/code/ex-37-sliding-window/example.py`**

```python
# pyright: strict
"""Example 37: Sliding-window rate limiter -- no boundary burst. (co-19)

A sliding window counts requests in a TRAILING window ending at NOW, so a
burst straddling a former boundary is still bounded by the limit (no 2x
flaw). This is the algorithm Cloudflare uses in production.
"""

from collections import deque  # => deque: efficient popleft of aged-out timestamps
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-19: keeps the timestamp of every call within the trailing window
class SlidingWindow:
    limit: int  # => max calls in ANY trailing window of `window_seconds`
    window_seconds: int  # => the trailing window length
    events: deque[int] = field(default_factory=deque[int])  # => call timestamps, oldest first


def allow(sw: SlidingWindow, now: int) -> bool:  # => co-19: count calls in [now-window, now]
    cutoff = now - sw.window_seconds  # => the oldest timestamp still inside the trailing window
    while sw.events and sw.events[0] <= cutoff:  # => drop timestamps that have aged out of the window
        sw.events.popleft()  # => remove the aged event
    if len(sw.events) >= sw.limit:  # => the trailing window is already full
        return False  # => denied
    sw.events.append(now)  # => record this call's timestamp
    return True  # => allowed


sw = SlidingWindow(limit=10, window_seconds=60)  # => co-19: 10 calls in any trailing 60s

# t=58: spend the whole limit at the tail of a span.
tail = sum(1 for _ in range(10) if allow(sw, now=58))  # => all 10 allowed
print(f"10 calls at t=58: allowed={tail}")  # => Output: 10

# t=60: only 2 seconds later, the trailing 60s window [0,60) STILL contains all 10 from t=58.
after = allow(sw, now=60)  # => co-19: the window is still full -> denied (no reset, no 2x burst)
print(f"call at t=60 (2s later): {after}")  # => Output: False -- the sliding window did NOT reset

# t=119: 61s after the t=58 burst, those calls have aged out -> room again.
freed = allow(sw, now=119)  # => co-19: the trailing window no longer holds the t=58 calls -> allowed
print(f"call at t=119 (61s after the burst): {freed}")  # => Output: True

assert tail == 10 and after is False and freed is True  # => co-19: avoids the fixed-window boundary burst
```

**Run**: `python3 example.py`

**Output**:

```text
10 calls at t=58: allowed=10
call at t=60 (2s later): False
call at t=119 (61s after the burst): True
```

**Key takeaway**: A sliding window counts the trailing window, so a boundary-straddling burst stays within the limit.

**Why it matters**: The sliding window trades a little more bookkeeping for correctness at the boundary.

---

### Example 38: 429 Too Many Requests + Retry-After

_ex-38 &middot; exercises co-20_

When a caller exceeds its rate limit, the response is 429 with a Retry-After header telling the caller how long to wait before retrying (RFC 6585 Sec 4).

**`learning/code/ex-38-rate-limit-429-retry-after/example.py`**

```python
# pyright: strict
"""Example 38: 429 Too Many Requests + Retry-After. (co-20)

When a caller exceeds its rate limit, the response is 429 with a Retry-After
header telling the caller how long to wait before retrying. Source: RFC 6585
Sec 4 (429) and RFC 9110 (Retry-After semantics).
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-20: status + headers (Retry-After lives here) + body
class Response:
    status: int  # => 200 when allowed, 429 when over the limit
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => carries Retry-After on a 429
    body: dict[str, str] = field(default_factory=dict[str, str])  # => a short message


BUDGET = [3]  # => a mutable budget cell: 3 calls allowed per window


def create_order() -> Response:  # => POST /orders -- rate-limited
    if BUDGET[0] <= 0:  # => co-20: over the limit -> 429
        return Response(status=429, headers={"Retry-After": "60"}, body={"error": "too many requests"})  # => 429 + hint
    BUDGET[0] -= 1  # => consume one unit of budget
    return Response(status=201, body={"status": "created"})  # => within budget -> 201


call_1 = create_order()  # => budget 3 -> 2
call_2 = create_order()  # => budget 2 -> 1
call_3 = create_order()  # => budget 1 -> 0
call_4 = create_order()  # => budget 0 -> over the limit
for i, resp in enumerate((call_1, call_2, call_3, call_4), start=1):
    retry = resp.headers.get("Retry-After", "-")  # => show Retry-After when present
    print(f"call {i}: status={resp.status}, Retry-After={retry}")  # => Output: 201,201,201,429

assert call_1.status == 201 and call_2.status == 201 and call_3.status == 201  # => the three compliant calls passed
assert call_4.status == 429 and call_4.headers["Retry-After"] == "60"  # => co-20: 429 carries a Retry-After hint
```

**Run**: `python3 example.py`

**Output**:

```text
call 1: status=201, Retry-After=-
call 2: status=201, Retry-After=-
call 3: status=201, Retry-After=-
call 4: status=429, Retry-After=60
```

**Key takeaway**: 429 carries a Retry-After hint -- actionable guidance, not a bare rejection.

**Why it matters**: Retry-After turns a throttle into a 'try again in N seconds' instruction a client can honor.

---

### Example 39: Cache-Aside -- Miss, DB, Populate, Then Hit

_ex-39 &middot; exercises co-21_

Cache-aside (lazy loading): on a cache MISS, read the DB, populate the cache, return; on a HIT, return straight from the cache. The DB query counter proves the second read never touches the DB (AWS caching strategies).

**`learning/code/ex-39-cache-aside-read/example.py`**

```python
# pyright: strict
"""Example 39: Cache-aside -- miss -> DB -> populate, then hit. (co-21)

Cache-aside (lazy loading): on a cache MISS, read the DB, populate the cache,
return the value; on a HIT, return straight from the cache. The DB query
counter proves the second read never touches the DB. Source: AWS Redis
caching strategies whitepaper (cache-aside / lazy load).
"""

from dataclasses import dataclass  # => a small typed record for the read result


DB_QUERY_COUNT = [0]  # => a mutable counter -- how many times the DB was actually queried
DB: dict[int, str] = {1: "Task A", 2: "Task B"}  # => the source of truth
CACHE: dict[int, str] = {}  # => co-21: the cache, populated lazily on a miss


@dataclass  # => co-21: distinguishes a cache hit from a miss
class ReadResult:
    value: str  # => the value returned
    source: str  # => "cache" or "db" -- proves which path served the read


def read_task(task_id: int) -> ReadResult:  # => GET /tasks/{id} -- cache-aside
    if task_id in CACHE:  # => co-21: HIT -> return straight from the cache
        return ReadResult(value=CACHE[task_id], source="cache")  # => no DB query
    DB_QUERY_COUNT[0] += 1  # => co-21: MISS -> query the DB (counted)
    value = DB[task_id]  # => the DB read
    CACHE[task_id] = value  # => co-21: populate the cache so the next read hits
    return ReadResult(value=value, source="db")  # => served from the DB this time


first = read_task(1)  # => MISS -> DB -> populate
print(f"first read:  value={first.value!r}, source={first.source}, db_queries={DB_QUERY_COUNT[0]}")  # => Output: db, 1

second = read_task(1)  # => HIT -> cache, no DB query
print(f"second read: value={second.value!r}, source={second.source}, db_queries={DB_QUERY_COUNT[0]}")  # => Output: cache, 1

assert first.source == "db" and second.source == "cache"  # => co-21: miss-then-hit
assert DB_QUERY_COUNT[0] == 1  # => the cached read issued ZERO additional DB queries
```

**Run**: `python3 example.py`

**Output**:

```text
first read:  value='Task A', source=db, db_queries=1
second read: value='Task A', source=cache, db_queries=1
```

**Key takeaway**: A miss loads the DB and populates the cache; the next read hits the cache and issues no query.

**Why it matters**: Lazy loading is the simplest caching strategy -- populate only what is actually read.

---

### Example 40: Cache-Aside -- a Cached Read Issues No DB Query

_ex-40 &middot; exercises co-21_

An instrumented DB proves a COLD read costs exactly one query, while every subsequent WARM read costs ZERO -- the cache absorbs the load the DB would otherwise see.

**`learning/code/ex-40-cache-aside-hit-no-db/example.py`**

```python
# pyright: strict
"""Example 40: Cache-aside -- a cached read issues no DB query. (co-21)

Same cache-aside pattern as Example 39, but the focus is the instrumented
DB: a COLD read costs exactly one query, while every subsequent WARM read
costs ZERO -- proving the cache absorbs the load the DB would otherwise see.
"""


class Database:  # => co-21: an instrumented DB that counts every query against it
    def __init__(self, rows: dict[int, str]) -> None:
        self._rows = rows  # => the source of truth
        self.queries = 0  # => the query counter

    def fetch(self, key: int) -> str | None:  # => each call is one real query
        self.queries += 1  # => count it
        return self._rows.get(key)  # => the value (or None)


class CacheAside:  # => co-21: the lazy-loading cache layer over the DB
    def __init__(self, db: Database) -> None:
        self._db = db  # => the backing store
        self._cache: dict[int, str] = {}  # => the cache, populated on a miss

    def read(self, key: int) -> str | None:  # => miss -> DB -> populate; hit -> cache
        if key in self._cache:  # => HIT
            return self._cache[key]  # => no DB query
        value = self._db.fetch(key)  # => MISS -> one DB query
        if value is not None:  # => only cache real values (not missing keys)
            self._cache[key] = value  # => populate
        return value  # => the value


db = Database({1: "Task A"})  # => co-21: an instrumented DB with one row
store = CacheAside(db)  # => the cache layer over it

cold = store.read(1)  # => MISS -> one DB query
warm = store.read(1)  # => HIT -> zero DB queries
warm2 = store.read(1)  # => HIT -> zero DB queries
print(f"cold read:  value={cold!r}, db.queries={db.queries}")  # => Output: 'Task A', 1
print(f"warm reads: value={warm!r}, db.queries={db.queries}")  # => Output: 'Task A', still 1

assert db.queries == 1  # => co-21: a cached read issues ZERO db queries; only the cold read cost one
assert cold == warm == warm2 == "Task A"  # => all three reads returned the same value
```

**Run**: `python3 example.py`

**Output**:

```text
cold read:  value='Task A', db.queries=1
warm reads: value='Task A', db.queries=1
```

**Key takeaway**: A cold read costs one query; every warm read costs zero -- the cache absorbs the DB load.

**Why it matters**: Measuring the query count makes the cache's value concrete rather than assumed.

---

### Example 41: Write-Through Cache

_ex-41 &middot; exercises co-22_

Write-through updates the cache SYNCHRONOUSLY on every write, so reads stay fresh without waiting for a TTL or a lazy reload (AWS caching strategies).

**`learning/code/ex-41-write-through/example.py`**

```python
# pyright: strict
"""Example 41: Write-through cache -- update cache and DB together. (co-22)

Write-through updates the cache SYNCHRONOUSLY on every write, so reads stay
fresh without waiting for a TTL or a lazy reload. Source: AWS Redis caching
strategies whitepaper (write-through).
"""

from dataclasses import dataclass  # => a small typed record for the read result


@dataclass  # => co-22: distinguishes a cache hit from a DB read
class ReadResult:
    value: str  # => the value returned
    source: str  # => "cache" or "db"


DB: dict[int, str] = {}  # => the durable store
CACHE: dict[int, str] = {}  # => co-22: kept IN SYNC with the DB on every write


def write_through(key: int, value: str) -> None:  # => co-22: update DB THEN cache, synchronously
    DB[key] = value  # => the durable write
    CACHE[key] = value  # => co-22: the cache is updated in the SAME operation -> reads stay fresh


def read(key: int) -> ReadResult:  # => a read always hits the fresh cache after a write-through
    if key in CACHE:  # => write-through keeps the cache populated
        return ReadResult(CACHE[key], "cache")  # => fresh, no DB read needed
    return ReadResult(DB.get(key, "<missing>"), "db")  # => cold cache fallback


write_through(1, "v1")  # => co-22: write updates BOTH DB and cache
read1 = read(1)  # => reads the FRESH value straight from the cache
print(f"after write-through: value={read1.value!r}, source={read1.source}")  # => Output: v1, cache

write_through(1, "v2")  # => co-22: a SECOND write rewrites BOTH -> cache is never stale
read2 = read(1)  # => reads the NEW value from the (synchronously updated) cache
print(f"after second write:  value={read2.value!r}, source={read2.source}")  # => Output: v2, cache

assert DB[1] == "v2" and CACHE[1] == "v2"  # => co-22: both reflect the latest write
assert read2.value == "v2" and read2.source == "cache"  # => reads are fresh, never stale
```

**Run**: `python3 example.py`

**Output**:

```text
after write-through: value='v1', source=cache
after second write:  value='v2', source=cache
```

**Key takeaway**: Write-through updates cache and DB together, so reads are always fresh.

**Why it matters**: Write-through trades a slightly slower write for never-stale reads.

---

### Example 42: Cache TTL Expiry

_ex-42 &middot; exercises co-23_

A TTL bounds how long a cached entry is considered fresh. After the TTL elapses, the entry EXPIRES and the next read re-loads from the DB.

**`learning/code/ex-42-cache-ttl-expiry/example.py`**

```python
# pyright: strict
"""Example 42: Cache TTL expiry -- entries expire and re-load. (co-23)

A TTL (time-to-live) bounds how long a cached entry is considered fresh.
After the TTL elapses, the entry EXPIRES and the next read re-loads from the
DB. The clock is INJECTED so the expiry is deterministic.
"""

from dataclasses import dataclass  # => a small typed record for a cache entry


@dataclass  # => co-23: a cached value plus the time it was cached
class Entry:
    value: str  # => the cached value
    cached_at: int  # => the (injected) clock time the entry was written


DB: dict[int, str] = {1: "fresh-from-db"}  # => the source of truth
CACHE: dict[int, Entry] = {}  # => co-23: the TTL-governed cache
TTL_SECONDS = 60  # => co-23: an entry is fresh for 60s after cached_at


def populate(key: int, now: int) -> None:  # => load a value into the cache
    CACHE[key] = Entry(value=DB[key], cached_at=now)  # => record the value AND when it was cached


def read(key: int, now: int) -> tuple[str, str]:  # => returns (value, source) honoring the TTL
    entry = CACHE.get(key)  # => look up the cached entry
    if entry is not None and now < entry.cached_at + TTL_SECONDS:  # => co-23: present AND within TTL -> fresh
        return entry.value, "cache"  # => served from cache
    CACHE.pop(key, None)  # => co-23: EXPIRED -> evict the stale entry
    populate(key, now)  # => re-load from the DB
    return DB[key], "db"  # => re-loaded


populate(1, now=0)  # => cache the value at t=0
within_ttl = read(1, now=30)  # => 30 < 0+60 -> still fresh
print(f"within TTL (t=30): value={within_ttl[0]!r}, source={within_ttl[1]}")  # => Output: fresh-from-db, cache

expired = read(1, now=70)  # => 70 >= 0+60 -> EXPIRED -> re-load
print(f"after TTL (t=70):  value={expired[0]!r}, source={expired[1]}")  # => Output: fresh-from-db, db

assert within_ttl[1] == "cache" and expired[1] == "db"  # => co-23: entry expired and re-loaded past the TTL
```

**Run**: `python3 example.py`

**Output**:

```text
within TTL (t=30): value='fresh-from-db', source=cache
after TTL (t=70):  value='fresh-from-db', source=db
```

**Key takeaway**: Past the TTL, an entry expires and the next read re-loads from the DB.

**Why it matters**: A TTL is a safety net for freshness when explicit invalidation is missed.

---

### Example 43: Explicit Cache Invalidation on a Mutation

_ex-43 &middot; exercises co-23_

A TTL alone cannot guarantee freshness if the DB changes before it expires. A write therefore EXPLICITLY invalidates (evicts) the cached key so the next read re-loads fresh.

**`learning/code/ex-43-cache-explicit-invalidate/example.py`**

```python
# pyright: strict
"""Example 43: Explicit cache invalidation on a mutation. (co-23)

A TTL alone cannot guarantee freshness if the DB changes before the TTL
expires. A write therefore EXPLICITLY invalidates (evicts) the cached key so
the next read re-loads the fresh value. "Cache invalidation is a correctness
problem" -- the wrong TTL serves stale data.
"""

DB: dict[int, str] = {1: "v1"}  # => the source of truth
CACHE: dict[int, str] = {1: "v1"}  # => co-23: a pre-populated cache


def read(key: int) -> tuple[str, str]:  # => returns (value, source)
    if key in CACHE:  # => hit
        return CACHE[key], "cache"  # => served from cache
    value = DB[key]  # => miss -> load from DB
    CACHE[key] = value  # => repopulate
    return value, "db"  # => re-loaded


def update(key: int, value: str) -> None:  # => a mutation that MUST invalidate the cache
    DB[key] = value  # => the durable write
    CACHE.pop(key, None)  # => co-23: EXPLICIT invalidation -- evict the now-stale entry


before = read(1)  # => served from the pre-populated cache
print(f"before update: value={before[0]!r}, source={before[1]}")  # => Output: v1, cache

update(1, "v2")  # => co-23: writes the DB AND invalidates the cached key
after = read(1)  # => cache was evicted -> re-loads the FRESH value from the DB
print(f"after update:  value={after[0]!r}, source={after[1]}")  # => Output: v2, db

assert DB[1] == "v2" and after[0] == "v2" and after[1] == "db"  # => co-23: invalidation forced a fresh re-load
assert 1 not in CACHE or CACHE[1] == "v2"  # => the cache no longer holds the stale "v1"
```

**Run**: `python3 example.py`

**Output**:

```text
before update: value='v1', source=cache
after update:  value='v2', source=db
```

**Key takeaway**: A mutation evicts the cached key, forcing the next read to re-load the fresh DB value.

**Why it matters**: Cache invalidation is a correctness problem -- explicit eviction on write is the disciplined fix.

---

### Example 44: The Stale-Data Bug -- a Too-Long TTL

_ex-44 &middot; exercises co-23_

A TTL longer than the data's real freshness window serves STALE data: the DB changes but the cache keeps returning the old value until the over-long TTL expires. This example shows the BUG, then the FIX.

**`learning/code/ex-44-cache-stale-bug/example.py`**

```python
# pyright: strict
"""Example 44: The stale-data bug -- a too-long TTL. (co-23)

A TTL longer than the data's real freshness window serves STALE data: the DB
changes but the cache keeps returning the old value until the (over-long) TTL
expires. This example shows the BUG, then applies the FIX (a correct TTL +
explicit invalidation).
"""

DB: dict[int, str] = {1: "v1"}  # => the source of truth
CACHE: dict[int, str] = {1: "v1"}  # => a pre-populated cache
CACHED_AT = [0]  # => when the cache entry was written (injected clock)
ttl_seconds = [9999]  # => co-23: the BUG -- a TTL far longer than the data's real freshness


def read_buggy(now: int) -> str:  # => the BUGGY read: trusts the over-long TTL
    entry_age = now - CACHED_AT[0]  # => how old the cached entry is
    if 1 in CACHE and entry_age < ttl_seconds[0]:  # => co-23: still "fresh" per the wrong TTL
        return CACHE[1]  # => BUG: returns STALE data after the DB changed
    return DB[1]  # => (unreachable while the buggy TTL holds)


DB[1] = "v2"  # => the DB changes -- but the cache is NOT invalidated
stale = read_buggy(now=10)  # => co-23: BUG -- age 10 < 9999, so "v1" is served from the stale cache
print(f"BUGGY (TTL=9999): DB is 'v2' but cache served {stale!r}")  # => Output: v1 (stale!)

# THE FIX: a correct TTL matching the freshness window, PLUS explicit invalidation on writes.
ttl_seconds[0] = 60  # => co-23: a TTL matching the real freshness window


def invalidate(key: int) -> None:  # => the FIX's other half -- evict on mutation
    CACHE.pop(key, None)  # => co-23: explicit invalidation


def read_fixed(now: int) -> str:  # => the FIXED read: correct TTL + invalidation
    entry_age = now - CACHED_AT[0]  # => age of the cached entry
    if 1 in CACHE and entry_age < ttl_seconds[0]:  # => within the CORRECT TTL -> fresh
        return CACHE[1]  # => fresh
    CACHE[1] = DB[1]  # => miss (evicted or expired) -> re-load the CURRENT DB value
    CACHED_AT[0] = now  # => record the reload time
    return CACHE[1]  # => the fresh value


invalidate(1)  # => co-23: the write path now invalidates the stale entry
fresh = read_fixed(now=10)  # => cache evicted -> re-loads the CURRENT DB value
print(f"FIXED (TTL=60 + invalidate): served {fresh!r}")  # => Output: v2 (fresh)

assert stale == "v1"  # => co-23: the bug served stale data
assert fresh == "v2"  # => co-23: the fix serves the fresh value
```

**Run**: `python3 example.py`

**Output**:

```text
BUGGY (TTL=9999): DB is 'v2' but cache served 'v1'
FIXED (TTL=60 + invalidate): served 'v2'
```

**Key takeaway**: A too-long TTL serves stale data after the DB changes; the fix is a correct TTL plus explicit invalidation.

**Why it matters**: Wrong TTLs are silent correctness bugs -- the cache looks healthy while serving stale data.

---

### Example 45: ETag + If-None-Match -> 304 Not Modified

_ex-45 &middot; exercises co-24_

The server tags a representation with an opaque ETag; a client resending If-None-Match with the SAME tag gets 304 (no body) when unchanged. A different tag -> 200 with the full body (RFC 9111).

**`learning/code/ex-45-etag-304/example.py`**

```python
# pyright: strict
"""Example 45: ETag + If-None-Match -> 304 Not Modified. (co-24)

The server tags a representation with an opaque ETag; a client resending
If-None-Match with the SAME tag gets 304 (no body) when the representation
is unchanged. A different tag -> 200 with the full body. Source: RFC 9111
(HTTP Caching, 2022).
"""

import hashlib  # => stdlib: derive a stable ETag from the representation


STORE: dict[int, str] = {1: "Hello, world"}  # => the resource


def etag_of(text: str) -> str:  # => co-24: a stable opaque tag derived from the representation
    return '"' + hashlib.sha256(text.encode()).hexdigest()[:16] + '"'  # => a quoted short hash


def get_with_etag(item_id: int, if_none_match: str | None) -> tuple[int, dict[str, str], str]:
    # => co-24: returns (status, headers, body)
    value = STORE.get(item_id, "")  # => the current representation
    current_etag = etag_of(value)  # => the current tag
    headers = {"ETag": current_etag}  # => every response carries the current tag
    if if_none_match == current_etag:  # => co-24: the client's tag MATCHES -> nothing changed
        return 304, headers, ""  # => 304, NO body
    return 200, headers, value  # => 200, full body


# First fetch: client has no tag -> full body + the new ETag.
status, headers, body = get_with_etag(1, if_none_match=None)
print(f"first fetch: status={status}, ETag={headers['ETag']}, body={body!r}")  # => Output: 200, full body

# Revalidation: client resends the SAME tag -> 304 (no body re-sent).
client_etag = headers["ETag"]  # => the tag the client remembered
status2, headers2, body2 = get_with_etag(1, if_none_match=client_etag)
print(f"revalidate (match): status={status2}, body={body2!r}")  # => Output: 304, empty body

# A stale tag (representation changed) -> 200 with the new body.
STORE[1] = "Hello, world (edited)"  # => the resource changed
status3, headers3, body3 = get_with_etag(1, if_none_match=client_etag)  # => old tag no longer matches
print(f"after change (stale tag): status={status3}, body={body3!r}")  # => Output: 200, new body

assert status == 200 and status2 == 304  # => co-24: match -> 304, no body re-sent
assert status3 == 200 and headers3["ETag"] != client_etag  # => co-24: changed -> new tag + full body
```

**Run**: `python3 example.py`

**Output**:

```text
first fetch: status=200, ETag="4ae7c3b6ac0beff6", body='Hello, world'
revalidate (match): status=304, body=''
after change (stale tag): status=200, body='Hello, world (edited)'
```

**Key takeaway**: A matching ETag returns 304 with no body -- saving the bandwidth of re-sending unchanged data.

**Why it matters**: ETag-based revalidation is HTTP caching's conditional-request mechanism.

---

### Example 46: Cache-Control: max-age

_ex-46 &middot; exercises co-24_

The Cache-Control: max-age=N directive tells a cache the representation is fresh for N seconds; within max-age it serves without revalidating, past max-age it must revalidate.

**`learning/code/ex-46-cache-control-maxage/example.py`**

```python
# pyright: strict
"""Example 46: Cache-Control: max-age. (co-24)

The Cache-Control: max-age=N directive tells a cache the representation is
fresh for N seconds. Within max-age the cache serves without revalidating;
past max-age the cache must revalidate. Source: RFC 9111.
"""

from dataclasses import dataclass  # => a small typed record for a cached representation


@dataclass  # => co-24: a representation plus when it was cached
class Cached:
    value: str  # => the representation
    cached_at: int  # => the (injected) clock time it was cached


CACHE: dict[int, Cached] = {}  # => a cache honoring Cache-Control


def serve(item_id: int, now: int) -> tuple[str, str]:  # => returns (value, source) honoring max-age
    max_age = 60  # => co-24: Cache-Control: max-age=60
    entry = CACHE.get(item_id)  # => look up the cached representation
    if entry is not None and now < entry.cached_at + max_age:  # => co-24: within max-age -> fresh, no revalidation
        return entry.value, "cache (within max-age)"  # => served fresh
    value = f"resource-{item_id}-at-{now}"  # => a fresh origin fetch (simulated)
    CACHE[item_id] = Cached(value, now)  # => cache it with the current time
    return value, "origin (past max-age or cold)"  # => had to revalidate


first = serve(1, now=0)  # => cold -> origin, cached at t=0
print(f"t=0:  {first}")  # => Output: origin

within = serve(1, now=30)  # => 30 < 0+60 -> fresh within max-age
print(f"t=30: {within}")  # => Output: cache (within max-age)

past = serve(1, now=70)  # => 70 >= 0+60 -> past max-age -> revalidate
print(f"t=70: {past}")  # => Output: origin (past max-age)

assert first[1].startswith("origin") and within[1].startswith("cache")  # => co-24: max-age honored within the window
assert past[1].startswith("origin")  # => co-24: past max-age, revalidation required
```

**Run**: `python3 example.py`

**Output**:

```text
t=0:  ('resource-1-at-0', 'origin (past max-age or cold)')
t=30: ('resource-1-at-0', 'cache (within max-age)')
t=70: ('resource-1-at-70', 'origin (past max-age or cold)')
```

**Key takeaway**: Within max-age a cache serves without asking the origin; past max-age it revalidates.

**Why it matters**: max-age lets a cache skip the conditional request entirely for a bounded window.

---

### Example 47: OpenTelemetry -- Recording a Span

_ex-47 &middot; exercises co-26_

OpenTelemetry is a vendor-neutral standard for traces, metrics, and logs. A SPAN records one unit of work (e.g. a handler) and may have child spans. This example simulates a tracer recording the span tree.

**`learning/code/ex-47-otel-span/example.py`**

```python
# pyright: strict
"""Example 47: OpenTelemetry -- recording a span. (co-26)

OpenTelemetry is a vendor-neutral standard for traces, metrics, and logs. A
SPAN records one unit of work (e.g. a handler) and may have child spans.
This example simulates a tracer that records spans in-process and verifies
the span tree is captured. Source: opentelemetry.io.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-26: one recorded span in the trace
class Span:
    name: str  # => the operation this span represents
    parent: str | None  # => the parent span's name (None for the root)
    attributes: dict[str, str] = field(default_factory=dict[str, str])  # => typed span attributes


class Tracer:  # => co-26: collects spans in-process (stands in for the OTel SDK)
    def __init__(self) -> None:
        self.finished: list[Span] = []  # => spans recorded so far

    def start_as_current(self, name: str, parent: str | None = None) -> "_SpanScope":  # => begin a span
        return _SpanScope(self, name, parent)  # => a context manager that finishes the span on exit


class _SpanScope:  # => co-26: a span's lifetime -- finishes (records) on __exit__
    def __init__(self, tracer: Tracer, name: str, parent: str | None) -> None:
        self._tracer = tracer  # => the tracer to record into
        self._span = Span(name=name, parent=parent)  # => the span being recorded

    def __enter__(self) -> Span:  # => entering the scope returns the live span
        return self._span  # => callers may set attributes on it

    def __exit__(self, *_exc: object) -> None:  # => leaving the scope finishes (records) the span
        self._tracer.finished.append(self._span)  # => co-26: the span is now recorded


tracer = Tracer()  # => co-26: one trace's collector

with tracer.start_as_current("GET /orders") as root:  # => the root span -- the handler
    root.attributes["http.method"] = "GET"  # => a typed attribute on the root span
    with tracer.start_as_current("db.query", parent="GET /orders") as child:  # => a child span -- the DB call
        child.attributes["db.system"] = "sqlite"  # => a typed attribute on the child span

recorded = tracer.finished  # => the spans the tracer captured
for span in recorded:  # => print the recorded span tree
    print(f"span: {span.name}, parent={span.parent}, attrs={span.attributes}")  # => Output: two spans

# Spans are recorded as they END -- a child (db.query) ends before its parent (GET /orders).
names = {s.name for s in recorded}  # => co-26: both spans recorded (order = end-order, child first)
assert names == {"GET /orders", "db.query"}  # => co-26: both spans recorded
db_span = next(s for s in recorded if s.name == "db.query")  # => find the child span
assert db_span.parent == "GET /orders"  # => co-26: the child's parent is the root span
```

**Run**: `python3 example.py`

**Output**:

```text
span: db.query, parent=GET /orders, attrs={'db.system': 'sqlite'}
span: GET /orders, parent=None, attrs={'http.method': 'GET'}
```

**Key takeaway**: A span records one unit of work; a child span nests under a parent in the trace.

**Why it matters**: Spans are the atomic unit of a distributed trace.

---

### Example 48: W3C Trace Context -- traceparent Propagation

_ex-48 &middot; exercises co-26_

A W3C traceparent header (version-traceid-spanid-flags) carries the trace identity across a service-to-service call, so a request can be followed across services (W3C Trace Context, Rec 2021).

**`learning/code/ex-48-traceparent-propagate/example.py`**

```python
# pyright: strict
"""Example 48: W3C Trace Context -- traceparent propagation. (co-26)

A W3C `traceparent` header (version-traceid-spanid-flags) carries the trace
identity across a service-to-service call so a request can be followed across
services. The downstream service extracts the SAME trace id. Source: W3C
Trace Context (Recommendation, 2021).
"""

from dataclasses import dataclass  # => a small typed record for a propagated context


@dataclass(frozen=True)  # => co-26: the identity propagated across one hop
class TraceContext:
    trace_id: str  # => the trace id -- the SAME across every hop in one request
    span_id: str  # => the span id -- a NEW one per hop
    flags: str  # => trace flags (e.g. sampled)


def make_traceparent(ctx: TraceContext) -> str:  # => co-26: serialize the context into the header
    return f"00-{ctx.trace_id}-{ctx.span_id}-{ctx.flags}"  # => version-traceid-spanid-flags


def parse_traceparent(header: str) -> TraceContext | None:  # => co-26: extract the context on the downstream side
    parts = header.split("-")  # => split the 4 dash-separated fields
    if len(parts) != 4:  # => malformed -> no context
        return None  # => reject
    _version, trace_id, span_id, flags = parts  # => the four fields
    return TraceContext(trace_id=trace_id, span_id=span_id, flags=flags)  # => the extracted context


# The upstream service starts a trace and propagates it to a downstream call.
upstream = TraceContext(trace_id="0af7651916cd43dd8448eb211c80319c", span_id="00f067aa0ba902b7", flags="01")  # => co-26
header = make_traceparent(upstream)  # => the traceparent header sent across the hop
print(f"upstream sends traceparent: {header}")  # => Output: the serialized header

# The downstream service receives the SAME trace id but records a NEW span id.
received = parse_traceparent(header)  # => co-26: extract on the downstream side
assert received is not None  # => type-narrow
downstream = TraceContext(trace_id=received.trace_id, span_id="e90a8f19a8bc4019", flags=received.flags)  # => new span, same trace
print(f"downstream trace_id: {downstream.trace_id}")  # => Output: the SAME trace id
print(f"downstream span_id:  {downstream.span_id} (new)")  # => Output: a NEW span id

assert downstream.trace_id == upstream.trace_id  # => co-26: the trace id is PRESERVED across the hop
assert downstream.span_id != upstream.span_id  # => co-26: each hop records its own span id
```

**Run**: `python3 example.py`

**Output**:

```text
upstream sends traceparent: 00-0af7651916cd43dd8448eb211c80319c-00f067aa0ba902b7-01
downstream trace_id: 0af7651916cd43dd8448eb211c80319c
downstream span_id:  e90a8f19a8bc4019 (new)
```

**Key takeaway**: A traceparent carries the SAME trace id across a hop -- each service records its own span id.

**Why it matters**: Without propagation, a trace ends at the first service boundary.

---

### Example 49: Health Check -- /livez (Liveness)

_ex-49 &middot; exercises co-27_

A liveness probe reports whether the process itself is healthy. A liveness FAILURE causes the orchestrator (kubelet) to RESTART the container.

**`learning/code/ex-49-health-liveness/example.py`**

```python
# pyright: strict
"""Example 49: Health check -- /livez (liveness). (co-27)

A liveness probe reports whether the process itself is healthy. A liveness
FAILURE causes the orchestrator (e.g. kubelet) to RESTART the container.
This example reports healthy normally, then unhealthy when an internal
liveness flag trips. Source: Kubernetes probes docs.
"""

from dataclasses import dataclass  # => a small typed response record


@dataclass  # => co-27: status + a short message
class Response:
    status: int  # => 200 healthy, 503 unhealthy
    body: dict[str, str]  # => a short status message


class Liveness:  # => co-27: the process's own internal liveness flag
    def __init__(self) -> None:
        self.alive = True  # => healthy until something fatal trips it

    def crash(self) -> None:  # => simulate a fatal internal condition
        self.alive = False  # => co-27: a liveness failure -> kubelet would RESTART


def livez(probe: Liveness) -> Response:  # => GET /livez
    if probe.alive:  # => co-27: process is alive
        return Response(200, {"status": "ok"})  # => 200 -- no restart needed
    return Response(503, {"status": "unhealthy"})  # => co-27: 503 -> triggers a container RESTART


probe = Liveness()  # => co-27: starts healthy
healthy = livez(probe)  # => alive -> 200
print(f"healthy: status={healthy.status}, body={healthy.body}")  # => Output: 200

probe.crash()  # => co-27: simulate a fatal condition
unhealthy = livez(probe)  # => not alive -> 503 (triggers restart)
print(f"after crash: status={unhealthy.status}, body={unhealthy.body}")  # => Output: 503

assert healthy.status == 200 and unhealthy.status == 503  # => co-27: liveness reports healthy then unhealthy
```

**Run**: `python3 example.py`

**Output**:

```text
healthy: status=200, body={'status': 'ok'}
after crash: status=503, body={'status': 'unhealthy'}
```

**Key takeaway**: A liveness failure restarts the container -- it asks 'is the process alive?'.

**Why it matters**: Liveness vs readiness is a real distinction: liveness restarts, readiness drops traffic.

---

### Example 50: Health Check -- /readyz (Readiness)

_ex-50 &middot; exercises co-27_

A readiness probe reports whether the pod is ready to receive traffic. A readiness FAILURE removes the pod from the Service's endpoints but does NOT restart it -- distinct from liveness.

**`learning/code/ex-50-health-readiness/example.py`**

```python
# pyright: strict
"""Example 50: Health check -- /readyz (readiness). (co-27)

A readiness probe reports whether the pod is ready to receive traffic. A
readiness FAILURE removes the pod from the Service's endpoints (it stops
getting requests) but does NOT restart it -- distinct from liveness. This
example shows unready while a dependency (DB) is down. Source: Kubernetes
probes docs.
"""

from dataclasses import dataclass  # => a small typed response record


@dataclass  # => co-27: status + a short message
class Response:
    status: int  # => 200 ready, 503 unready
    body: dict[str, str]  # => a short status message


class Readiness:  # => co-27: tracks whether dependencies are available
    def __init__(self) -> None:
        self.db_up = True  # => the dependency's availability

    def db_goes_down(self) -> None:  # => simulate a dependency outage
        self.db_up = False  # => co-27: dependency down -> unready (but NOT a restart)

    def db_recovers(self) -> None:  # => simulate the dependency recovering
        self.db_up = True  # => ready again


def readyz(probe: Readiness) -> Response:  # => GET /readyz
    if not probe.db_up:  # => co-27: dependency down -> unready
        return Response(503, {"status": "unready", "reason": "db down"})  # => 503 -> removed from endpoints, NOT restarted
    return Response(200, {"status": "ready"})  # => 200 -> receives traffic


probe = Readiness()  # => co-27: starts ready (dependency up)
ready = readyz(probe)  # => db up -> 200
print(f"ready: status={ready.status}, body={ready.body}")  # => Output: 200

probe.db_goes_down()  # => co-27: dependency outage -> unready (not restarted)
unready = readyz(probe)  # => db down -> 503
print(f"db down: status={unready.status}, body={unready.body}")  # => Output: 503, removed from endpoints

probe.db_recovers()  # => dependency recovers -> ready again (no restart was needed)
recovered = readyz(probe)  # => db up -> 200
print(f"recovered: status={recovered.status}, body={recovered.body}")  # => Output: 200

assert ready.status == 200 and unready.status == 503 and recovered.status == 200  # => co-27: readiness tracks the dependency
```

**Run**: `python3 example.py`

**Output**:

```text
ready: status=200, body={'status': 'ready'}
db down: status=503, body={'status': 'unready', 'reason': 'db down'}
recovered: status=200, body={'status': 'ready'}
```

**Key takeaway**: A readiness failure removes the pod from endpoints WITHOUT restarting -- it asks 'can I take traffic?'.

**Why it matters**: Restarting on a dependency outage (a readiness concern) is wrong -- you'd thrash instead of waiting it out.

---

### Example 51: GraphQL -- a Client Selects Exactly the Fields It Needs

_ex-51 &middot; exercises co-07_

GraphQL exposes ONE endpoint where the client's QUERY names which fields to return, solving REST's over/under-fetching.

**`learning/code/ex-51-graphql-query/example.py`**

```python
# pyright: strict
"""Example 51: GraphQL -- a client selects exactly the fields it needs. (co-07)

GraphQL exposes ONE endpoint where the client's QUERY names which fields to
return, solving REST's over/under-fetching. This example resolves ONLY the
requested fields from a single record.
"""

from typing import Any  # => a GraphQL response is arbitrary nested JSON


ARTICLE: dict[str, object] = {"id": 1, "title": "Hello, GraphQL", "body": "A long article body...", "author": "ada"}  # => the full record


def resolve_article(requested_fields: list[str]) -> dict[str, Any]:  # => co-07: the query picks the fields
    selected = {field: ARTICLE[field] for field in requested_fields if field in ARTICLE}  # => co-07: ONLY requested fields
    return {"data": {"article": selected}}  # => wrapped in GraphQL's own data envelope


narrow = resolve_article(["title"])  # => co-07: ask for ONLY title
print(f"query {['title']!r}:       {narrow}")  # => Output: only the title field

two_fields = resolve_article(["id", "title"])  # => co-07: ask for two fields
print(f"query {['id','title']!r}: {two_fields}")  # => Output: exactly those two fields

assert narrow["data"]["article"] == {"title": "Hello, GraphQL"}  # => co-07: only the requested field returns
assert set(two_fields["data"]["article"].keys()) == {"id", "title"}  # => co-07: no body/author leaked through
```

**Run**: `python3 example.py`

**Output**:

```text
query ['title']:       {'data': {'article': {'title': 'Hello, GraphQL'}}}
query ['id', 'title']: {'data': {'article': {'id': 1, 'title': 'Hello, GraphQL'}}}
```

**Key takeaway**: A GraphQL query returns ONLY the fields the caller asked for -- no more, no less.

**Why it matters**: Field selection is GraphQL's core answer to REST's fixed-shape over-fetching.

---

### Example 52: REST Over-Fetches; GraphQL Does Not

_ex-52 &middot; exercises co-07_

The SAME data served via a fixed-shape REST response returns EVERY field whether the caller needs them or not. A GraphQL query selecting a subset returns ONLY those fields. The byte counts make the gap concrete.

**`learning/code/ex-52-graphql-overfetch-contrast/example.py`**

```python
# pyright: strict
"""Example 52: REST over-fetches; GraphQL does not. (co-07)

The SAME underlying data served via a fixed-shape REST response returns
EVERY field whether the caller needs them or not (over-fetching). A GraphQL
query selecting a subset returns ONLY those fields. The field/byte counts
make the gap concrete.
"""

import json  # => stdlib: count response bytes


ARTICLE: dict[str, object] = {"id": 1, "title": "Hello, GraphQL", "body": "A long article body...", "author": "ada"}  # => the full record


def rest_response() -> dict[str, object]:  # => co-07: REST returns a FIXED shape -- every field, every time
    return ARTICLE  # => the caller gets body+author even if it only wanted the title


def graphql_response(requested: list[str]) -> dict[str, object]:  # => co-07: GraphQL returns ONLY the requested fields
    return {field: ARTICLE[field] for field in requested if field in ARTICLE}  # => caller-shaped


rest = rest_response()  # => the caller only wanted the title, but REST sent everything
gql = graphql_response(["title"])  # => co-07: GraphQL sends exactly what was asked for

rest_bytes = len(json.dumps(rest))  # => the bytes REST sent
gql_bytes = len(json.dumps(gql))  # => the bytes GraphQL sent
print(f"REST returned {len(rest)} fields / {rest_bytes} bytes: {rest}")  # => Output: 4 fields, full payload
print(f"GraphQL returned {len(gql)} fields / {gql_bytes} bytes: {gql}")  # => Output: 1 field, tiny payload
print(f"GraphQL saved {rest_bytes - gql_bytes} bytes ({(1 - gql_bytes / rest_bytes) * 100:.0f}%) for this caller")  # => Output: the over-fetch gap

assert len(rest) == 4 and len(gql) == 1  # => co-07: REST over-fetched; GraphQL did not
assert gql_bytes < rest_bytes  # => co-07: the caller-shaped query transferred strictly fewer bytes
```

**Run**: `python3 example.py`

**Output**:

```text
REST returned 4 fields / 87 bytes: {'id': 1, 'title': 'Hello, GraphQL', 'body': 'A long article body...', 'author': 'ada'}
GraphQL returned 1 fields / 27 bytes: {'title': 'Hello, GraphQL'}
GraphQL saved 60 bytes (69%) for this caller
```

**Key takeaway**: REST returns a fixed shape (over-fetching); GraphQL returns the caller's subset (fewer bytes).

**Why it matters**: Over-fetching is a real latency-and-bandwidth cost on constrained clients (mobile).

---

### Example 53: GraphQL N+1 Resolver, Then a DataLoader Batch

_ex-53 &middot; exercises co-07, co-40_

A naive resolver fetches each item's related author ONE AT A TIME -- 1 query for the list plus N per-item queries (the N+1 problem). A DataLoader-style batch collapses all N lookups into ONE bulk query.

**`learning/code/ex-53-graphql-n-plus-1/example.py`**

```python
# pyright: strict
"""Example 53: GraphQL N+1 resolver, then a DataLoader batch. (co-07, co-40)

A naive resolver fetches each item's related author ONE AT A TIME across a
list -- 1 query for the list plus N per-item queries (the N+1 problem). A
DataLoader-style batch collapses all N lookups into ONE bulk query. The query
counter proves the drop. co-40 also names the batching fix for the N+1 query.
"""

from dataclasses import dataclass  # => a typed article record avoids dict[int|str] typing pitfalls

QUERY_COUNT = [0]  # => a mutable counter -- how many queries were issued


@dataclass  # => one article, with a slot to hold the resolved author
class Article:
    id: int  # => the article id
    author_id: int  # => the related author to resolve
    author: str = ""  # => filled in by the resolver (empty until resolved)


def fetch_articles() -> list[Article]:  # => the list query (1 query)
    QUERY_COUNT[0] += 1  # => count it
    return [Article(1, 10), Article(2, 20), Article(3, 30)]  # => 3 articles


def fetch_author_naive(author_id: int) -> str:  # => the NAIVE per-item resolver (1 query EACH)
    QUERY_COUNT[0] += 1  # => count each individual lookup
    return f"Author-{author_id}"  # => the resolved author


def fetch_authors_batch(author_ids: list[int]) -> dict[int, str]:  # => co-07/co-40: the DataLoader-style BATCH (1 query)
    QUERY_COUNT[0] += 1  # => ONE bulk query for ALL the ids
    return {aid: f"Author-{aid}" for aid in author_ids}  # => all authors in one shot


# --- The N+1 pattern: 1 (list) + 3 (one per article) = 4 queries. ---
QUERY_COUNT[0] = 0  # => reset
articles = fetch_articles()  # => 1 query
for a in articles:  # => for EACH article...
    a.author = fetch_author_naive(a.author_id)  # => ...one MORE query (N+1)
n_plus_1 = QUERY_COUNT[0]  # => 1 + 3 = 4
print(f"N+1 resolver: {n_plus_1} queries for {len(articles)} articles")  # => Output: 4

# --- The DataLoader fix: 1 (list) + 1 (batch) = 2 queries. ---
QUERY_COUNT[0] = 0  # => reset
articles = fetch_articles()  # => 1 query
author_ids = [a.author_id for a in articles]  # => collect ALL author ids first
authors = fetch_authors_batch(author_ids)  # => co-07/co-40: ONE bulk query for every id
for a in articles:  # => assign from the pre-fetched batch
    a.author = authors[a.author_id]  # => no per-item query
batched = QUERY_COUNT[0]  # => 1 + 1 = 2
print(f"DataLoader batch: {batched} queries for {len(articles)} articles")  # => Output: 2

assert n_plus_1 == 4 and batched == 2  # => co-07/co-40: N+1 collapsed from 4 to a constant 2
```

**Run**: `python3 example.py`

**Output**:

```text
N+1 resolver: 4 queries for 3 articles
DataLoader batch: 2 queries for 3 articles
```

**Key takeaway**: The N+1 issues 1+N queries; the DataLoader batch collapses it to a constant 2.

**Why it matters**: The N+1 is GraphQL's classic performance trap; batching is the universal fix (also co-40).

---

### Example 54: gRPC Unary RPC

_ex-54 &middot; exercises co-08_

gRPC uses Protocol Buffers as BOTH the IDL and the wire format over HTTP/2. A UNARY RPC is one request -> one response.

**`learning/code/ex-54-grpc-unary/example.py`**

```python
# pyright: strict
"""Example 54: gRPC unary RPC -- request/response round-trip. (co-08)

gRPC uses Protocol Buffers as BOTH the interface-definition language and the
wire format, over HTTP/2. A UNARY RPC is one request -> one response. This
example simulates the protobuf service/handler in-process and verifies the
round-trip. Source: gRPC over HTTP/2 + Protobuf.
"""

from dataclasses import dataclass  # => a small typed record standing in for a protobuf message


@dataclass  # => co-08: a protobuf-message-like request
class EchoRequest:
    message: str  # => the payload the client sends


@dataclass  # => co-08: a protobuf-message-like response
class EchoResponse:
    message: str  # => the payload the server returns


class EchoService:  # => co-08: the gRPC service stub (stands in for generated code)
    def unary_echo(self, request: EchoRequest) -> EchoResponse:  # => co-08: a UNARY RPC -- one request, one response
        return EchoResponse(message=f"echo:{request.message}")  # => the single response


service = EchoService()  # => the server-side service instance
response = service.unary_echo(EchoRequest(message="hello"))  # => co-08: client sends one request
print(f"unary request:  {EchoRequest('hello')}")  # => Output: the request
print(f"unary response: {response}")  # => Output: one response
assert response.message == "echo:hello"  # => co-08: the request/response round-tripped
```

**Run**: `python3 example.py`

**Output**:

```text
unary request:  EchoRequest(message='hello')
unary response: EchoResponse(message='echo:hello')
```

**Key takeaway**: A unary RPC is one request, one response -- Protobuf-typed over HTTP/2.

**Why it matters**: Protobuf-as-IDL-and-wire is a different contract model from REST's OpenAPI-plus-JSON.

---

### Example 55: gRPC Server-Streaming RPC

_ex-55 &middot; exercises co-08_

A server-streaming RPC takes ONE request and returns a STREAM of messages -- useful for a large or incrementally-produced result set.

**`learning/code/ex-55-grpc-streaming/example.py`**

```python
# pyright: strict
"""Example 55: gRPC server-streaming RPC. (co-08)

A server-streaming RPC takes ONE request and returns a STREAM of messages
(useful for a large or incrementally-produced result set). This example
simulates the stream as a generator and verifies multiple messages arrive
in order. Source: gRPC over HTTP/2.
"""

from collections.abc import Iterator  # => Iterator: the type of a streaming RPC's message stream
from dataclasses import dataclass  # => a small typed record standing in for a protobuf message


@dataclass  # => co-08: the streaming request (asks for N log lines)
class LogRequest:
    count: int  # => how many log lines the client wants


@dataclass  # => co-08: one streamed log-line message
class LogLine:
    seq: int  # => the sequence number of this line in the stream
    text: str  # => the line's content


class LogService:  # => co-08: the gRPC service with a server-streaming method
    def stream_logs(self, request: LogRequest) -> Iterator[LogLine]:  # => co-08: ONE request -> MANY streamed responses
        for seq in range(1, request.count + 1):  # => produce each line in order
            yield LogLine(seq=seq, text=f"log line {seq}")  # => one streamed message


service = LogService()  # => the server-side service
stream = service.stream_logs(LogRequest(count=4))  # => co-08: client sends one request
lines = list(stream)  # => collect every streamed message
for line in lines:  # => print them as they arrived
    print(f"received: seq={line.seq}, text={line.text!r}")  # => Output: 4 lines, in order

assert [line.seq for line in lines] == [1, 2, 3, 4]  # => co-08: multiple messages streamed back, in order
```

**Run**: `python3 example.py`

**Output**:

```text
received: seq=1, text='log line 1'
received: seq=2, text='log line 2'
received: seq=3, text='log line 3'
received: seq=4, text='log line 4'
```

**Key takeaway**: A server-streaming RPC returns many messages in order from one request.

**Why it matters**: Streaming lets a server push incremental results instead of buffering the whole set.

---

### Example 56: REST vs GraphQL vs gRPC -- the Same Operation Three Ways

_ex-56 &middot; exercises co-07, co-08_

The SAME fetch expressed three ways: a fixed-shape REST JSON response, a caller-shaped GraphQL field selection, and a typed gRPC unary RPC. Each works; the note names when each fits.

**`learning/code/ex-56-rest-vs-graphql-vs-grpc/example.py`**

```python
# pyright: strict
"""Example 56: REST vs GraphQL vs gRPC -- the same operation three ways. (co-07, co-08)

The SAME fetch (get an article's title) expressed three ways: a fixed-shape
REST JSON response, a caller-shaped GraphQL field selection, and a typed gRPC
unary RPC. Each works; the printed note names when each style fits.
"""

from dataclasses import dataclass  # => a small typed record for the gRPC message
from typing import Any  # => GraphQL/REST responses are arbitrary nested JSON

RECORD: dict[str, object] = {"id": 1, "title": "Same data, three styles", "body": "..."}  # => the single source of truth


def rest_fetch() -> dict[str, object]:  # => co-07: REST -- a fixed-shape JSON response (cacheable via GET)
    return RECORD  # => returns every field


def graphql_fetch(requested: list[str]) -> dict[str, Any]:  # => co-07: GraphQL -- the caller picks fields (no over-fetch)
    return {field: RECORD[field] for field in requested if field in RECORD}  # => caller-shaped


@dataclass  # => co-08: a typed protobuf-like message
class ArticleRequest:
    article_id: int  # => the id to fetch


@dataclass  # => co-08: a typed protobuf-like response
class ArticleResponse:
    title: str  # => a single typed field


def grpc_fetch(request: ArticleRequest) -> ArticleResponse:  # => co-08: gRPC -- a typed unary RPC over HTTP/2
    return ArticleResponse(title=str(RECORD["title"]))  # => a typed response (binary on the wire in real gRPC)


rest = rest_fetch()  # => co-07: works -- best for public, cacheable APIs
gql = graphql_fetch(["title"])  # => co-07: works -- best when callers need different shapes
rpc = grpc_fetch(ArticleRequest(1))  # => co-08: works -- best for typed internal service-to-service calls
print(f"REST title:     {rest['title']}")  # => Output: Same data, three styles
print(f"GraphQL title:  {gql['title']}")  # => Output: Same data, three styles
print(f"gRPC title:     {rpc.title}")  # => Output: Same data, three styles
print("each fits: REST=cacheable/public, GraphQL=caller-shaped, gRPC=typed/internal")  # => Output: when each wins

assert rest["title"] == gql["title"] == rpc.title  # => co-07/co-08: the same data, three working styles
```

**Run**: `python3 example.py`

**Output**:

```text
REST title:     Same data, three styles
GraphQL title:  Same data, three styles
gRPC title:     Same data, three styles
each fits: REST=cacheable/public, GraphQL=caller-shaped, gRPC=typed/internal
```

**Key takeaway**: The same operation works three ways -- REST for cacheable/public, GraphQL for caller-shaped, gRPC for typed/internal.

**Why it matters**: No style is a strict upgrade; each is correct for specific forces.

---

← Previous: [Beginner Examples](./beginner.md) · Next: [Advanced Examples](./advanced.md) →
