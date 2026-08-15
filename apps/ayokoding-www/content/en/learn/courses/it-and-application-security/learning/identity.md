---
title: "Cryptography and identity"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

## Choose a property before a primitive

Cryptography protects a stated property under stated assumptions. These examples distinguish secrecy,
integrity, authentication, and authorization before showing minimal local mechanisms. The programs
are demonstrations of library use, not production key-management systems.

### Worked Example 19: Compare hashing and encryption

**Context**: A password verifier and a document archive have different jobs.

| Need                          | Appropriate operation     | Can original be recovered? |
| ----------------------------- | ------------------------- | -------------------------- |
| Verify password               | slow salted password hash | no                         |
| Read protected document later | authenticated encryption  | yes, with key              |

**Key takeaway**: Hashing verifies without recovery; encryption protects data that must be recovered.

**Why It Matters**: Storing an encrypted password creates a decryption target and misses the point of
password verification. Hashing a document makes it impossible to read later. Start with the data
lifecycle before selecting an API. (co-16)

### Worked Example 20: Encrypt symmetrically

**Context**: The runnable example creates a fresh key, encrypts a synthetic note, and decrypts it.

Run: `python3 learning/code/ex-20-symmetric-encryption.py`

**Key takeaway**: Symmetric encryption uses the same secret key to protect and recover data.

**Why It Matters**: Modern authenticated-encryption libraries protect both secrecy and tamper
detection when used as designed. The hard part in production is key lifecycle, access, rotation, and
recovery—not inventing a cipher around a string operation. (co-17, co-21)

### Worked Example 21: Assign asymmetric roles

**Context**: A public key can be distributed while the private key remains under one owner's control.

| Operation                       | Key used              |
| ------------------------------- | --------------------- |
| Sign a release manifest         | private key           |
| Verify that manifest            | public key            |
| Encrypt a message for recipient | recipient public key  |
| Decrypt that message            | recipient private key |

**Key takeaway**: Public/private pairs separate verification or encryption access from private control.

**Why It Matters**: The key roles are not interchangeable labels. A system that exports a private
key to every verifier loses the boundary that makes signatures and recipient encryption useful.
(co-17)

### Worked Example 22: Choose Argon2id parameters

**Context**: A password hash needs deliberate memory, time, and parallelism settings.

Run: `python3 learning/code/ex-22-23-passwords.py`

**Key takeaway**: Argon2id with 19 MiB memory, two iterations, and one lane is an OWASP minimum-tier
baseline, to be measured against the service's own login budget.

**Why It Matters**: Password hashes should be expensive for offline guessing but acceptable during
legitimate sign-in. The encoded hash carries its parameters, allowing a future login to detect and
upgrade an older policy. (co-18)

### Worked Example 23: Reject a wrong password

**Context**: The same runnable program verifies the correct synthetic passphrase and rejects another.

Run: `python3 learning/code/ex-22-23-passwords.py`

**Key takeaway**: Verification compares a candidate to the stored Argon2id result; plaintext is not
retrieved or stored.

**Why It Matters**: A login response should be generic whether the account is unknown or the
candidate is wrong. That prevents a normal authentication decision from becoming an account-enumeration
oracle while retaining useful internal observability. (co-18)

### Worked Example 24: Explain salting

**Context**: Two users choose the same password; the password hasher creates different stored values.

`argon2id("same password", random salt A) ≠ argon2id("same password", random salt B)`

**Key takeaway**: A unique random salt prevents identical passwords from sharing a precomputed result.

**Why It Matters**: Salt is not secret and is normally stored with the encoded hash. Its value is
forcing attackers to pay the derivation cost per account instead of reusing one rainbow-table lookup.
(co-18)

### Worked Example 25: Verify a digital signature

**Context**: The local program signs a synthetic message and proves altered bytes fail verification.

Run: `python3 learning/code/ex-25-signature.py`

**Key takeaway**: A signature binds the private-key holder to the exact message bytes verified by a
public key.

**Why It Matters**: Signatures supply integrity and an attribution property only while private-key
access, key identity, and revocation are governed. They do not make a malicious but correctly signed
message safe or replace authorization. (co-19)

### Worked Example 26: Bound non-repudiation claims

**Context**: A release is signed by a service account whose private key is available to a small team.

| Evidence            | What it supports            | What it does not prove        |
| ------------------- | --------------------------- | ----------------------------- |
| Valid signature     | controlled key signed bytes | which human pressed approve   |
| Protected audit log | event sequence              | truth of every business claim |

**Key takeaway**: Non-repudiation depends on identity and key custody beyond the algorithm.

**Why It Matters**: Overstating a signature's legal or operational meaning creates false assurance.
Pair it with access control, time-stamped audit records, approval policy, and a key-compromise response.
(co-19)

### Worked Example 27: Read a TLS handshake goal

**Context**: A client establishes a modern HTTPS connection to an API.

`client hello → server certificate and key agreement → verified encrypted application data`

**Key takeaway**: TLS combines authenticated key establishment, confidentiality, and integrity for
the connection.

**Why It Matters**: HTTPS is not merely URL decoration. Certificate validation prevents an active
network attacker from substituting a server; disabling it to "fix" a local error removes that core
property. (co-20)

### Worked Example 28: Follow a certificate chain

**Context**: A browser validates a service certificate through an intermediate CA to a trusted root.

| Certificate        | Signed by    | Role                |
| ------------------ | ------------ | ------------------- |
| `api.example` leaf | intermediate | identifies endpoint |
| intermediate       | root         | delegates issuance  |
| root               | trust store  | trust anchor        |

**Key takeaway**: A chain is trusted only when validation reaches an appropriate local trust anchor.

**Why It Matters**: A certificate's subject name, validity period, chain, and revocation information
all participate in the decision. Copying a certificate file or ignoring hostname mismatch does not
produce a secure connection. (co-20)

### Worked Example 29: Refuse homemade crypto

**Context**: A developer proposes XOR-ing data with a repeating key before storage.

| Proposal                     | Review result                                     |
| ---------------------------- | ------------------------------------------------- |
| Repeating-key transformation | reject: no authenticated encryption or key design |
| Maintained AEAD library      | use with documented key management                |

**Key takeaway**: A small cipher-like function is not a cryptographic system.

**Why It Matters**: Secure construction needs nonce handling, authentication, side-channel resistance,
key rotation, and review that ad-hoc code rarely gets. Use maintained primitives with a narrow,
well-documented interface. (co-21)

### Worked Example 30: Split authentication from authorization

**Context**: A valid employee session requests an approver-only receipt action.

| Check          | Question                             | Result     |
| -------------- | ------------------------------------ | ---------- |
| Authentication | Who made this request?               | employee A |
| Authorization  | May employee A approve this receipt? | no         |

**Key takeaway**: Authentication establishes identity; authorization decides the permitted action.

**Why It Matters**: A correct login can coexist with a serious access-control failure. Keep both
decisions visible in designs and tests so a feature does not mistake “signed in” for “allowed.”
(co-22)

### Worked Example 31: Name OAuth 2.0 roles

**Context**: An expense app delegates access to an identity platform.

| Role                 | Example           |
| -------------------- | ----------------- |
| Resource owner       | employee          |
| Client               | expense web app   |
| Authorization server | identity provider |
| Resource server      | receipt API       |

**Key takeaway**: OAuth 2.0 delegates authorization among four distinct roles.

**Why It Matters**: Naming roles prevents a browser client from being confused with a resource
server or an identity provider. It also makes token audience, redirect, and consent decisions
reviewable instead of implicit. (co-23)

### Worked Example 32: Choose a grant

**Context**: A user-facing app and a nightly internal job have different delegation needs.

| Situation                                | Grant fit                    |
| ---------------------------------------- | ---------------------------- |
| Employee signs into browser app          | authorization code with PKCE |
| Service calls its own API without a user | client credentials           |

**Key takeaway**: Grant type follows the actor and trust boundary, not implementation convenience.

**Why It Matters**: A client-credentials token cannot stand in for a human consent flow, and a
browser must not be entrusted with a client secret. OAuth 2.1 remains an IETF draft; use published
OAuth 2.0 standards and current BCPs as the stable reference. (co-23)

### Worked Example 33: Read JWT structure

**Context**: A token has `header.payload.signature` segments.

| Segment   | Purpose                           |
| --------- | --------------------------------- |
| Header    | fixed algorithm and token type    |
| Payload   | claims such as subject and expiry |
| Signature | integrity over header and payload |

**Key takeaway**: A JWT is signed claims, not encrypted claims by default.

**Why It Matters**: Anyone holding a typical signed JWT can decode its payload. Put no secrets in
claims and validate issuer, audience, expiry, signature, and an application-selected algorithm before
using any authorization claim. (co-24)

### Worked Example 34: Detect token tampering

**Context**: The runnable demonstration issues a fixed-HS256 synthetic token and rejects changed bytes.

Run: `python3 learning/code/ex-34-jwt-integrity.py`

**Key takeaway**: Verification recomputes a signature with a server-held key and compares it safely.

**Why It Matters**: This compact example teaches integrity only. A production token verifier should
use a maintained JWT library and additionally enforce key selection, issuer, audience, expiration,
and revocation policy. (co-24)

### Worked Example 35: Reject algorithm confusion

**Context**: A verifier receives a token whose header asks for `none` or a different algorithm.

`accepted algorithms = {"HS256"}; token header algorithm ∉ set → reject`

**Key takeaway**: The verifier selects accepted algorithms; token input never selects verification policy.

**Why It Matters**: Treating an untrusted header as configuration can remove verification or mix
incompatible key types. Pin the algorithm in code or trusted configuration and reject every unexpected
header before reading claims. (co-24)

### Worked Example 36: Set session-cookie flags

**Context**: An application sets a browser session cookie.

`Set-Cookie: session=<opaque>; Secure; HttpOnly; SameSite=Lax; Path=/`

**Key takeaway**: `Secure` limits transport, `HttpOnly` limits script access, and `SameSite` helps
limit cross-site sending.

**Why It Matters**: These flags are complementary. They do not replace TLS, output encoding, session
rotation, or server-side authorization, but they remove common browser paths for leaking or replaying a
session identifier. (co-25)

### Worked Example 37: Budget session entropy

**Context**: A session identifier is generated with `secrets.token_urlsafe(16)`.

`16 random bytes = 128 bits before encoding`

**Key takeaway**: An opaque session ID needs enough unpredictable entropy, not an incrementing number.

**Why It Matters**: OWASP specifies at least 64 bits of entropy; a larger standard-library random
token gives practical margin. Entropy is only one control: expire, rotate after login, invalidate on
logout, and protect the cookie transport. (co-25)

### Worked Example 38: Distinguish XSS forms

**Context**: Untrusted text reaches a browser through three paths.

| Form      | Path                                       |
| --------- | ------------------------------------------ |
| Reflected | request value immediately rendered         |
| Stored    | saved comment later rendered               |
| DOM       | client script writes unsafe value into DOM |

**Key takeaway**: XSS origin changes, but each form crosses into an executable browser context.

**Why It Matters**: Defenses must match the actual rendering context—HTML text, attribute, URL, CSS,
or JavaScript—and use safe framework APIs. A browser-side sanitizer cannot repair unsafe server
templating automatically. (co-13)

## Sources

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
  documents Argon2id parameter guidance.
- [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) defines OAuth 2.0 roles and grants;
  [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) defines the identity layer.
- [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519) defines JWT, and
  [RFC 9846](https://www.rfc-editor.org/rfc/rfc9846) is the current TLS 1.3 specification.
