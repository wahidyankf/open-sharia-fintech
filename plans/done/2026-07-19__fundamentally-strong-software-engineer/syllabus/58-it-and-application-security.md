# 58 · IT / Application Security (Annotated-concept, Python \*)

**prd row**: Pass 3 · Build for the Real World · Annotated-concept · Python \* · Learn 158 / Drill 258 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the security body of knowledge an engineer needs — the CIA triad, threat modeling
(STRIDE), the OWASP Top 10 (2025), applied cryptography (hashing/symmetric/asymmetric/TLS), identity
(OAuth2/OIDC deepened), and secure-SDLC practices. `*`: Python where a mechanism is shown runnably (e.g. a
password-hash verifier, a JWT check), else annotated. This is the conceptual spine feeding the two hands-on
security topics — [`59-offensive-security`](./59-offensive-security.md) and
[`60-defensive-security`](./60-defensive-security.md) — and it deepens
[`17-security-essentials`](./17-security-essentials.md).

## Why this exists · the big idea

- **The problem before the solution**: security isn't a feature you add — it's a property that fails at the
  weakest point, and an attacker needs only one gap while you must hold all of them.
- **Keep-this-if-you-forget-everything**: think in threats and layers — model what can go wrong (STRIDE),
  assume any single control fails (defense in depth), grant the least privilege that works, and never invent
  your own crypto.
- **Big ideas touched**: `layering-and-leaks` (defense in depth assumes each layer leaks),
  `correctness-vs-pragmatism` (threat modeling prioritizes risk; perfect security is not the goal),
  `mechanism-vs-policy` (least privilege and access control are policy enforced by mechanism).

## Prerequisites

- **Prior topics**: [topic 17 Security Essentials](./17-security-essentials.md) (auth, hashing, injection
  basics), [topic 39 Backend at Scale](./39-backend-at-scale.md) (OAuth2/OIDC, the surface to secure), and
  [topic 4 Just Enough Python](./04-just-enough-python.md).
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** with pinned CVE-clean crypto/JWT libs
  (never roll your own crypto); a Markdown editor for the threat model. All work against your own code/data
  only.
- **Assumed knowledge**: tokens vs sessions + password hashing (topic 17); OAuth2/OIDC at a using level
  (topic 39); Python basics (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: **OWASP Top 10:2025** released and current. Order: A01 Broken Access Control,
  A02 Security Misconfiguration, A03 **Software Supply Chain Failures (new)**, A04 Cryptographic Failures,
  A05 Injection, A06 Insecure Design, A07 Authentication Failures (renamed), A08 Software/Data Integrity
  Failures, A09 Security Logging & Alerting Failures (renamed), A10 **Mishandling of Exceptional Conditions
  (new)**; SSRF folded into A01. STRIDE remains the dominant threat-model mnemonic (extended for AI, not
  superseded). (owasp.org/Top10/2025)
- 2026-07-12 — verified: Argon2id baseline `m=19456 KiB (19 MiB), t=2, p=1` (alt `m=47104, t=1, p=1`),
  OWASP first-choice hash. TLS 1.3 preferred, TLS 1.2 the accepted floor. RSA ≥ 2048-bit floor per NIST
  SP 800-131A Rev. 2 (still the finalized rev; Rev. 3 in draft — teaching guidance "RSA ≥ 2048, prefer
  ECC/larger" unaffected). (cheatsheetseries.owasp.org / csrc.nist.gov)
- 2026-07-12 — verified (CORRECTION of framing): **OAuth 2.1 is NOT a ratified RFC** — it is an active IETF
  draft (`draft-ietf-oauth-v2-1-15`, 2026-03-02). Phrase it as "OAuth 2.1 (IETF draft consolidating OAuth
  2.0 + current security BCPs)," not a finalized standard co-equal with RFC 6749. (datatracker.ietf.org)

### DD-35 primary-source citations (fetched-and-read)

> Every framework name, control count, and standard below traces to a primary source the author fetched
> and READ. Unverifiable specifics carry `[Needs Verification]`.

- **CIA triad** `[Verified]` — [NIST SP 800-12 Rev. 1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-12r1.pdf)
  §1.4 (verbatim, sourced from CNSSI 4009): Confidentiality = "Preserving authorized restrictions on
  information access and disclosure…"; Integrity = "Guarding against improper information modification or
  destruction and ensuring information non-repudiation and authenticity"; Availability = "Ensuring timely and
  reliable access to and use of information." Corroborated by [FIPS 199](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.199.pdf) p. 2 (44 U.S.C. §3542).
- **TLS 1.3 — CURRENT SPEC IS RFC 9846, NOT RFC 8446** `[Verified]` — [RFC 9846](https://www.rfc-editor.org/rfc/rfc9846)
  (2026) verbatim: "This document obsoletes RFC 8446, which specified TLS 1.3." Any content citing RFC 8446 as
  "the TLS 1.3 spec" is now `[Outdated]`. Handshake/CA framing corroborated by [MDN TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security).
- **OWASP Top 10:2025** `[Verified]` — [owasp.org/Top10/2025](https://owasp.org/Top10/2025/) fetched; A01–A10
  list verbatim-matches this file's note above. Injection def (A05) verbatim: "untrusted user input… sent to
  an interpreter… causes the interpreter to execute parts of that input as commands." Broken Access Control
  (A01) core sentence is word-for-word identical between the 2021 and 2025 editions (stable teaching quote).
  Exact GA calendar date `[Needs Verification]` (RC 2025-11-06, GA early 2026 per secondary sources only).
- **CWE weakness IDs** `[Verified]` — [CWE-89 SQLi](https://cwe.mitre.org/data/definitions/89.html),
  [CWE-78 OS Command Injection](https://cwe.mitre.org/data/definitions/78.html),
  [CWE-284 Improper Access Control](https://cwe.mitre.org/data/definitions/284.html),
  [CWE-79 XSS](https://cwe.mitre.org/data/definitions/79.html) (Type-0/1/2 = DOM/Reflected/Stored, verbatim),
  [CWE-352 CSRF](https://cwe.mitre.org/data/definitions/352.html),
  [CWE-311](https://cwe.mitre.org/data/definitions/311.html)/[CWE-327](https://cwe.mitre.org/data/definitions/327.html)
  (crypto) — all fetched at CWE v4.20.
- **Password storage** `[Verified]` — [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html):
  Argon2id "minimum configuration of 19 MiB of memory, an iteration count of 2, and 1 degree of parallelism";
  bcrypt "work factor of 10 or more and with a password limit of 72 bytes"; salt = "a unique, randomly
  generated string… added to each password."
- **AuthN vs AuthZ** `[Verified]` — NIST CSRC glossary: [authentication](https://csrc.nist.gov/glossary/term/authentication)
  = "Verifying the identity of a user, process, or device…"; [authorization](https://csrc.nist.gov/glossary/term/authorization)
  = "The right or a permission that is granted to a system entity to access a system resource."
- **OAuth 2.0 / JWT / OIDC** `[Verified]` — [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) §1.1 (4 roles:
  resource owner, resource server, client, authorization server) + §1.3 (grant types);
  [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519) JWT = "a compact, URL-safe means of representing claims…";
  [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) = "a simple identity layer
  on top of the OAuth 2.0 protocol."
- **Session security** `[Verified]` — [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html):
  "Session identifiers must have at least 64 bits of entropy"; `Secure`/`HttpOnly`/`SameSite` flag semantics
  verbatim.
- **Security headers** `[Verified]` — MDN: [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)
  ("a defense against cross-site scripting (XSS) attacks"),
  [HSTS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security)
  (`preload` needs `max-age>=31536000` + `includeSubDomains`),
  [X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options)
  (`nosniff`), [X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options)
  (`DENY`/`SAMEORIGIN`; `ALLOW-FROM` obsolete → CSP `frame-ancestors`). OWASP Secure Headers Project landing
  page is now a thin GitHub pointer — MDN is the stronger primary here.
- **STRIDE** `[Verified]` — [Microsoft Learn — Threat Modeling Tool Threats](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats):
  Spoofing/Tampering/Repudiation/Information Disclosure/Denial of Service/Elevation of Privilege, each with a
  verbatim definition; "a core element of the Microsoft Security Development Lifecycle (SDL)."
- **Secure SDLC** `[Verified]` — [NIST SP 800-218 (SSDF v1.1)](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf):
  practice groups "Prepare the Organization (PO)" and "Protect Software (PS)" confirmed verbatim from Table 1
  (note "Protect Software", not "Protect **the** Software"); PW/RV group wording `[Needs Verification]`.
- **CVE/CVSS/NVD** `[Verified]` — [NVD CVE process](https://nvd.nist.gov/general/cve-process): CVE = "a
  dictionary or glossary of vulnerabilities that have been identified for specific code bases";
  [FIRST CVSS](https://www.first.org/cvss/) current version = **v4.0**. Direct cve.org verbatim quote
  `[Needs Verification]` (fetch timed out; NVD is the primary substitute).
- **GDPR** `[Verified]` — [EUR-Lex Reg. (EU) 2016/679](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02016R0679-20160504)
  Art. 4(1): personal data = "any information relating to an identified or identifiable natural person."
- **Defense in depth / least privilege** `[Verified]` — NIST CSRC glossary:
  [defense-in-depth](https://csrc.nist.gov/glossary/term/defense_in_depth) = "multiple layers… attacks missed
  by one technology are caught by another"; [least privilege](https://csrc.nist.gov/glossary/term/least_privilege)
  = "restrict the access privileges… to the minimum necessary to accomplish assigned tasks." Full SP 800-53
  AC-6 control text `[Needs Verification]` (glossary definition suffices for conceptual framing).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Annotated-concept). Each example below cites the co-NN it exercises. -->

- **co-01 · cia-triad** — Confidentiality, Integrity, and Availability are the three properties every security control ultimately serves.
- **co-02 · defense-in-depth** — layered controls where each layer is assumed to leak, so a second catches what the first misses.
- **co-03 · least-privilege** — grant the minimum access needed to do the job, and no more.
- **co-04 · threat-modeling-stride** — STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) is the prompt to enumerate what can go wrong.
- **co-05 · attack-surface-trust-boundary** — the entry points and trust boundaries where untrusted input crosses into trusted code.
- **co-06 · risk-likelihood-impact** — prioritize threats by likelihood × impact rather than treating all as equal.
- **co-07 · owasp-top-10** — the OWASP Top 10 (2025) is a prioritized, breach-data-driven map of the risks that actually happen.
- **co-08 · broken-access-control** — A01: missing/incorrect authorization checks, IDOR, and vertical vs horizontal privilege escalation (CWE-284).
- **co-09 · injection** — A05: untrusted input executed as a command because data and command are not kept separate (CWE-89/77/78).
- **co-10 · cryptographic-failures** — A04: sensitive data left unencrypted at rest or in transit, or protected with broken algorithms (CWE-311/327).
- **co-11 · security-misconfiguration** — A02: default credentials, verbose errors, and unhardened defaults as an exploitable gap.
- **co-12 · supply-chain-failures** — A03 (new 2025): vulnerable or malicious third-party dependencies and the SCA that finds them.
- **co-13 · xss** — cross-site scripting (stored/reflected/DOM), defended by context-specific output encoding and CSP (CWE-79).
- **co-14 · csrf** — cross-site request forgery, defended by synchronizer anti-CSRF tokens and SameSite cookies (CWE-352).
- **co-15 · input-validation** — allowlist validation (define what IS allowed) beats denylist filtering (trivially bypassable).
- **co-16 · hashing-vs-encryption** — hashing is one-way (verify, don't recover); encryption is reversible (protect, then recover).
- **co-17 · symmetric-vs-asymmetric** — symmetric uses one shared key; asymmetric uses a public/private keypair.
- **co-18 · password-hashing** — store passwords with a slow, salted KDF (argon2id baseline m=19 MiB, t=2, p=1), never plaintext or fast hashes.
- **co-19 · digital-signatures** — sign with a private key and verify with the public key, giving integrity and non-repudiation.
- **co-20 · tls-https** — TLS secures a connection via encryption, integrity, and certificate-based authentication anchored to a CA (RFC 9846).
- **co-21 · dont-roll-your-own-crypto** — use vetted, maintained crypto libraries; homemade ciphers fail.
- **co-22 · authentication-vs-authorization** — authentication verifies identity; authorization grants permission to a resource.
- **co-23 · oauth2-oidc** — OAuth 2.0 delegates authorization across four roles and several grant types; OIDC adds an identity layer on top (RFC 6749).
- **co-24 · jwt** — a JSON Web Token carries signed claims (header.payload.signature); its pitfalls include alg:none and weak secrets (RFC 7519).
- **co-25 · session-security** — session IDs need ≥64 bits of entropy and Secure/HttpOnly/SameSite cookie flags.
- **co-26 · secrets-management** — never hardcode secrets; store them in a vault/env, restrict access, and rotate them.
- **co-27 · security-headers** — HTTP security headers (CSP, HSTS, X-Content-Type-Options, X-Frame-Options) add browser-enforced defenses.
- **co-28 · secure-sdlc** — shift security left: SAST/DAST/SCA gates in the pipeline per a secure-development framework (NIST SSDF).
- **co-29 · cve-cvss-nvd** — read a CVE/advisory and reason about exploitability using its CVSS score and NVD enrichment.
- **co-30 · data-protection-privacy** — PII and privacy obligations (GDPR personal-data scope, breach duties) shape what must be protected.

## Worked examples

Colocated under `it-security/learning/`; annotated threat models + tables/diagrams + runnable Python security
mechanisms (DD-20/DD-30). Contiguous `ex-01..ex-52`. Every example cites the `co-NN` it exercises. Concepts
come before examples.

### Beginner

- **ex-01 · cia-triad-table** — annotate a table mapping an asset to its C/I/A impact — verify each dimension has a concrete loss scenario. (co-01)
- **ex-02 · cia-tradeoff** — annotate a case where availability trades against confidentiality — verify the tension is named. (co-01)
- **ex-03 · defense-in-depth-layers** — annotate a diagram of layered controls — verify each layer is assumed to leak. (co-02)
- **ex-04 · least-privilege-grant** — annotate a least-privilege grant vs an over-broad one — verify the minimized scope. (co-03)
- **ex-05 · stride-categories** — annotate the six STRIDE categories with one threat each — verify all six appear. (co-04)
- **ex-06 · stride-threat-model** — a STRIDE threat model over a login flow — verify each entry point has a threat + mitigation. (co-04, co-05)
- **ex-07 · trust-boundary-diagram** — annotate a data-flow diagram with trust boundaries — verify each boundary crossing. (co-05)
- **ex-08 · attack-surface-enum** — enumerate the attack surface of an endpoint — verify inputs/outputs are listed. (co-05)
- **ex-09 · risk-prioritization** — annotate a likelihood × impact risk matrix — verify high-risk items rank first. (co-06)
- **ex-10 · owasp-top10-map** — annotate the OWASP Top 10:2025 list as a prioritized map — verify all ten categories present. (co-07)
- **ex-11 · broken-access-idor** — annotate an IDOR accessing another user's record — verify the missing authorization check. (co-08)
- **ex-12 · vertical-vs-horizontal-privesc** — annotate vertical vs horizontal privilege escalation — verify the distinction. (co-08)
- **ex-13 · sql-injection-anatomy** — annotate a SQL injection turning data into command — verify the injected clause. (co-09)
- **ex-14 · parameterized-query-fix** — a parameterized query fixing the injection in Python — verify data stays separate from command. (co-09)
- **ex-15 · command-injection** — annotate an OS command injection — verify untrusted input reaching the shell. (co-09)
- **ex-16 · security-misconfig** — annotate a misconfiguration (default creds / verbose errors) — verify the hardening fix. (co-11)
- **ex-17 · input-validation-allowlist** — an allowlist input validator in Python — verify unauthorized input is rejected. (co-15)
- **ex-18 · denylist-bypass** — annotate why a denylist filter is bypassable — verify a bypass case. (co-15)

### Intermediate

- **ex-19 · hashing-vs-encryption** — annotate hashing (one-way) vs encryption (reversible) — verify the irreversibility of the hash. (co-16)
- **ex-20 · symmetric-encrypt** — a symmetric encrypt/decrypt round-trip in Python — verify the plaintext is recovered. (co-17)
- **ex-21 · asymmetric-keypair** — annotate a public/private keypair — verify which key encrypts vs decrypts. (co-17)
- **ex-22 · argon2id-hash** — hash a password with argon2id (m=19 MiB, t=2, p=1) — verify the parameters. (co-18)
- **ex-23 · argon2id-verify** — verify a correct password and reject a wrong one in Python — verify accept/reject. (co-18)
- **ex-24 · salting** — annotate why a per-password salt defeats rainbow tables — verify the unique salt. (co-18)
- **ex-25 · digital-signature-verify** — sign a message and verify it in Python — verify a tampered message fails. (co-19)
- **ex-26 · non-repudiation** — annotate how a signature gives non-repudiation — verify the property. (co-19)
- **ex-27 · tls-handshake** — annotate the TLS 1.3 handshake steps — verify version + cipher + key agreement. (co-20)
- **ex-28 · certificate-chain** — annotate a certificate chain to a CA — verify the trust anchor. (co-20)
- **ex-29 · dont-roll-crypto** — annotate a broken homemade cipher vs a vetted library — verify the failure. (co-21)
- **ex-30 · authn-vs-authz** — annotate authentication vs authorization on one request — verify the two distinct checks. (co-22)
- **ex-31 · oauth2-roles** — annotate the four OAuth2 roles on an authorization-code flow — verify each role. (co-23)
- **ex-32 · oauth2-grant-types** — annotate authorization-code vs client-credentials grants — verify when each applies. (co-23)
- **ex-33 · jwt-structure** — annotate a JWT's header/payload/signature — verify the three parts. (co-24)
- **ex-34 · jwt-tamper-detect** — verify a valid JWT and reject a tampered one in Python — verify tamper detection. (co-24)
- **ex-35 · jwt-alg-none-pitfall** — annotate the alg:none / weak-secret JWT pitfall — verify the rejection. (co-24)
- **ex-36 · session-cookie-flags** — annotate Secure/HttpOnly/SameSite on a session cookie — verify each flag's effect. (co-25)
- **ex-37 · session-entropy** — annotate the ≥64-bit session-ID entropy requirement — verify unpredictability. (co-25)
- **ex-38 · xss-reflected-vs-stored** — annotate reflected vs stored vs DOM XSS — verify the three types. (co-13)

### Advanced

- **ex-39 · xss-output-encoding** — annotate context-specific output encoding fixing XSS — verify the encoded context. (co-13)
- **ex-40 · csp-header** — annotate a Content-Security-Policy blocking inline script — verify the XSS defense. (co-13, co-27)
- **ex-41 · csrf-token** — annotate a synchronizer anti-CSRF token — verify a per-session unpredictable token. (co-14)
- **ex-42 · samesite-cookie** — annotate SameSite=Lax/Strict as CSRF defense-in-depth — verify cross-site suppression. (co-14, co-25)
- **ex-43 · crypto-failure-at-rest** — annotate missing encryption at rest — verify the exposed data. (co-10)
- **ex-44 · security-headers-set** — annotate HSTS + X-Content-Type-Options + X-Frame-Options — verify each header's effect. (co-27)
- **ex-45 · secrets-no-hardcode** — annotate a hardcoded secret moved to a vault/env — verify no secret remains in code. (co-26)
- **ex-46 · secret-rotation** — annotate a secret-rotation flow — verify the old secret is invalidated. (co-26)
- **ex-47 · supply-chain-sca** — annotate an SCA scan flagging a vulnerable dependency — verify the CVE match. (co-12)
- **ex-48 · secure-sdlc-shift-left** — annotate SAST/DAST/SCA placed early in the pipeline (shift-left) — verify each gate's stage. (co-28)
- **ex-49 · cve-read** — annotate reading a CVE record (description + references) — verify the affected component. (co-29)
- **ex-50 · cvss-score** — annotate a CVSS Base score's severity — verify the metric group. (co-29)
- **ex-51 · pii-gdpr** — annotate PII under GDPR Art. 4 + the breach-notification duty — verify the personal-data scope. (co-30)
- **ex-52 · secure-assessment-capstone** — the full assessment: STRIDE + OWASP map + crypto mechanisms + SDLC checklist — verify each part is present. (co-01, co-04, co-07, co-18, co-24, co-28)

## Tensions & trade-offs — when NOT to reach for this

- **Security vs usability/velocity**: every control (MFA, least privilege, short token TTLs, strict CSP) adds
  friction for users and developers; maximum security ships nothing and protects no one. The trade is
  calibrated to the asset's value and threat model, not maxed.
- **Threat modeling can over- or under-reach**: model too shallow and you miss the real attack; enumerate
  every theoretical threat and you drown in low-risk noise. STRIDE is a prompt to prioritize by
  likelihood × impact, not a checklist to exhaustively satisfy.
- **When NOT to max it**: a public read-only marketing site and a payments backend sit at opposite ends of
  the risk spectrum. Right-size the controls to what is actually at stake rather than applying one bar
  everywhere.

## Lineage — why it beat the alternative

- The engineering-security canon is scar tissue from public breaches. The CIA triad and defense-in-depth come
  from military/infosec doctrine; the OWASP Top 10 (from 2003, revised on real-world breach data — the 2025
  list adds supply-chain failures after SolarWinds and the xz backdoor) codifies the attacks that actually
  happen; "don't roll your own crypto" is the lesson of a thousand broken homemade ciphers. Each item earned
  its place by causing damage — so the list is a prioritized map of where effort pays off. It feeds directly
  into the hands-on red/blue topics [`59-offensive-security`](./59-offensive-security.md) and
  [`60-defensive-security`](./60-defensive-security.md).

## Capstone materials

Colocated under `it-security/learning/`; annotated threat models + runnable Python security mechanisms
(DD-20/DD-30).

- **threat-model** — a STRIDE threat model for the backend app, annotated (assets, entry points, threats,
  mitigations).
- **crypto-mechanisms** — runnable Python: verify an argon2id password hash; verify/reject a tampered JWT;
  a digital-signature verify.
- **owasp-walkthrough** — an annotated mapping of the OWASP Top 10 (2025) to concrete code smells +
  fixes in the app.

## Capstone spec — intra-topic (subject → threat-model artifact + runnable mechanisms)

- **Goal**: produce a complete security assessment of the backend app — a STRIDE threat model mapping
  assets/entry-points/threats/mitigations, a mapping of the OWASP Top 10 (2025) to the app with concrete
  prevention notes, and a set of runnable Python mechanisms (argon2id hash verify, tamper-detecting JWT
  check, a signature verify) — the conceptual + hands-on backbone the red/blue topics build on.
- **Concepts exercised**: [ ] a STRIDE threat model (co-04, co-05) [ ] OWASP Top 10 (2025) mapped to the app
  (co-07, co-08, co-09, co-13) [ ] password hashing done right (argon2id) (co-18) [ ] JWT tamper detection
  (co-24) [ ] a digital-signature verify (co-19) [ ] a secure-SDLC checklist (deps/secrets/headers) (co-26,
  co-27, co-28).
- **Ordered steps**:
  1. `.../learning/capstone/threat-model.md` — STRIDE over the app: assets, entry points, per-category
     threats + mitigations. Verify every entry point has at least one identified threat + mitigation.
  2. `.../learning/capstone/code/crypto.py` — argon2id verify + a JWT integrity check. Verify a correct
     password/token passes and a tampered one is rejected.
  3. `owasp-2025.md` — each Top-10 category mapped to a concrete place in the app + its prevention. Verify
     every category is addressed (present or justified N/A).
  4. `secure-sdlc.md` — a dependency/supply-chain + secrets + security-headers checklist run against the
     app. Verify each item has a concrete status.
- **Acceptance criteria**: the threat model covers every entry point; the OWASP 2025 mapping is complete;
  the crypto mechanisms correctly accept valid and reject tampered inputs; the secure-SDLC checklist is
  filled with concrete statuses.
- **Done bar**: threat-model artifact complete + mechanisms runnable + web-verified (esp. OWASP 2025 list).

## Read more

**Books**

- **The Web Application Hacker's Handbook** — Dafydd Stuttard, Marcus Pinto (2nd ed., 2011). The standard practitioner reference for web application security testing and secure design.
- **Security Engineering** — Ross Anderson (3rd ed., 2020). Comprehensive reference covering the full breadth of security engineering, cryptography, and systems design, freely distributed by the author. <https://www.cl.cam.ac.uk/~rja14/book.html>

**Papers & articles**

- **OWASP Top 10** — OWASP Foundation (ongoing). The canonical, community-consensus list of critical web application security risks. <https://owasp.org/www-project-top-ten/>
- **NIST Cybersecurity Framework (CSF) 2.0** — National Institute of Standards and Technology (2024). The widely adopted US government reference framework for organizational cybersecurity risk management. <https://www.nist.gov/cyberframework>

---

← Previous: [57 · Agentic AI](./57-agentic-ai.md) · Next: [59 · Offensive Security](./59-offensive-security.md) →
