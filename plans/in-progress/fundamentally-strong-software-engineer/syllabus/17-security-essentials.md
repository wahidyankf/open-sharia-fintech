# 17 · Security Essentials (By Example, Python)

**prd row**: Pass 1 · Core Foundations · By Example · Python · Learn 117 / Drill 217 · Nvim-ready
Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the **usable slice** — the everyday security a developer applies to the software they just
learned to build: the OWASP-style top risks, safe input handling, auth done right, secret hygiene, and
dependency safety. Threat modeling, cryptographic depth, and org-scale controls go to
[`58-it-and-application-security`](./58-it-and-application-security.md) and [`60-defensive-security`](./60-defensive-security.md) (DD-11).
This topic closes Pass 1 and anchors two inter-topic capstones.

## Why this exists · the big idea

- **The problem before the solution**: the software you just learned to build trusts its inputs by
  default, and every trusted-but-hostile input is an attack — security is the discipline of not trusting.
- **Keep-this-if-you-forget-everything**: validate at the boundary and grant least privilege — treat every
  input as hostile until proven safe, and give every component only the access it needs.
- **Big ideas touched**: `layering-and-leaks` — a vulnerability is a trust boundary that leaked (injection
  is the data/code layer bleeding through); `mechanism-vs-policy` — authentication is the mechanism, and
  least-privilege authorization is the policy you lay over it.

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./04-just-enough-python.md),
  [topic 10 SQL Essentials](./10-sql-essentials.md) (SQL-injection examples), and
  [topic 11 Backend Essentials](./11-backend-essentials.md) — the HTTP service you built there is the
  application these attacks/defenses target.
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x**; the Backend-Essentials app + its DB;
  **`curl`** to send malicious/edge requests; a pinned CVE-clean password-hash library (**argon2**/bcrypt);
  a dependency-audit CLI (**`pip-audit`**).
- **Assumed knowledge**: reading/writing Python; issuing HTTP requests with `curl`; basic SQL and a
  parameterized query (topic 10); how a request reaches a handler (topic 11).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (CORRECTION): **OWASP Top 10:2025** is now current (published Jan 2026, supersedes
  2021). Order: A01 Broken Access Control, A02 Security Misconfiguration, A03 **Software Supply Chain
  Failures (new)**, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication
  Failures, A08 Software/Data Integrity Failures, A09 Security Logging & Alerting Failures, A10
  **Mishandling of Exceptional Conditions (new, replaces SSRF)**. Author against 2025 wording/order.
  (owasp.org Top10/2025)
- 2026-07-12 — verified: Argon2id min-tier params `m=19456 (19 MiB), t=2, p=1`; bcrypt work factor min 10
  (as high as perf allows), hard 72-byte input limit. `pip-audit` **2.10.1** (latest; reads requirements/
  pyproject/venv against the PyPA Advisory DB by default, OSV available as an alternate `-s osv` source,
  needs Python ≥3.10). Parameterized-query guidance unchanged. (cheatsheetseries.owasp.org / pypi.org)
- 2026-07-15 — re-verified (independent second pass, no corrections needed to either prior bullet):
  OWASP Top 10:2025 ordering/names confirmed unchanged against owasp.org/Top10/2025/. Pinned versions to
  author this topic's examples against, confirmed current on PyPI today: **argon2-cffi 25.1.0**,
  **bcrypt 5.0.0**, **PyJWT 2.13.0**, **pip-audit 2.10.1**, **detect-secrets 1.5.0** (no new PyPI release
  since 2024-05-06 — flagged stale-but-still-maintained upstream, not abandoned; author against 1.5.0 and
  note the freshness caveat rather than treating the version as evergreen), **cyclonedx-bom 7.3.0**
  (installs the `cyclonedx-py` CLI command — the separate `cyclonedx-py` PyPI package is a thin pointer
  package, do not install it directly), **Flask 3.1.3** (bundles Jinja2 3.1.6, Werkzeug 3.1.8, MarkupSafe
  3.0.3, itsdangerous 2.2.0), **pydantic 2.13.4**, **flask-limiter 4.1.1**, **fakeredis 2.36.2** (in-memory
  Redis stand-in, keeps the distributed-rate-limit example self-contained with no external service).
  **PyJWT CVE-2026-32597** (CVSS 7.5, HIGH — `crit` header parameter, RFC 7515 §4.1.11, not validated):
  affects PyJWT ≤2.11.0, fixed in 2.12.0; current 2.13.0 is unaffected — pin PyJWT to `>=2.12.0`, author
  against 2.13.0, and use the CVE itself as a one-line "why pin exact versions" aside in the JWT examples.
  No other CVEs found against the pinned versions above. (owasp.org/Top10/2025 · pypi.org ·
  github.com/advisories/GHSA-752w-5fwx-jx9f · nvd.nist.gov/vuln/detail/CVE-2026-32597 ·
  pyjwt.readthedocs.io · developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS ·
  flask.palletsprojects.com/en/stable/web-security/)
- 2026-07-16 — re-verified for Phase 19 (`capstone-first-working-software`, the Pass-1 inter-topic
  capstone anchored in this file's "Capstone spec" section below): every version this capstone's Python
  stack reuses is current and CVE-clean today. **FastAPI 0.139.0** (2026-07-01), **uvicorn 0.51.0**
  (2026-07-08, `[standard]` extras), **pydantic 2.13.4** (2026-05-06), **argon2-cffi 25.1.0**
  (2025-06-03, no known CVEs), **pytest 9.1.1** (2026-06-19), **Hypothesis 6.156.6** (2026-07-10, no
  known CVEs), **pip-audit 2.10.1** (2026-06-10), **coverage.py 7.15.2** (topic 15 co-21, verified via
  `pip index versions coverage` against PyPI directly at authoring time, no known CVEs) — all confirmed
  current on PyPI, no regressions since the 2026-07-15 sweep above. **New finding**: Starlette's `TestClient` (imported by FastAPI's own
  testing docs) now tries `import httpx2 as httpx` first, falling back to plain `httpx` with a
  `StarletteDeprecationWarning` — confirmed by fetching Starlette's `testclient.py` source directly.
  `httpx2` **2.7.0** (2026-07-14) is a genuine PyPI package, drop-in-API-compatible with `httpx`, now
  maintained by Pydantic Services Inc. as `httpx`'s de facto successor (upstream `httpx` has not
  released since 0.28.1, 2024-12-06). FastAPI's own published testing docs have not yet been updated to
  mention `httpx2` (still say `pip install httpx`) — this repo's own `security-essentials` capstone
  already pinned `httpx2==2.7.0` for the same reason (2026-07-15 entry above); this capstone's
  `requirements.txt` does the same for consistency. Python: **3.13.12** (the exact interpreter used for
  every real run captured on this capstone's page — CPython's own downloads page lists 3.14.6 as the
  newest stable line and 3.13.x as the actively-patched N-1 line as of today; 3.13 remains a fully
  supported, CVE-clean choice, matching the interpreter this whole Pass-1 track's other capstone already
  ran against). (pypi.org/project/fastapi · pypi.org/project/uvicorn · pypi.org/project/pydantic ·
  pypi.org/project/argon2-cffi · pypi.org/project/pytest · pypi.org/project/hypothesis ·
  pypi.org/project/pip-audit · pypi.org/project/httpx2 ·
  raw.githubusercontent.com/encode/starlette/master/starlette/testclient.py ·
  fastapi.tiangolo.com/tutorial/testing/ · python.org/downloads)

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject By-Example). Each example below cites the co-NN it exercises. -->

- **co-01 · trust-boundaries-never-trust-input** — every place untrusted data crosses into your code (query, form, header, cookie, upstream response) is a boundary where it must be validated; the default posture is distrust.
- **co-02 · owasp-top-10-as-risk-map** — the OWASP Top 10:2025 is a shared risk vocabulary that maps a concrete bug to a named category, prioritizing what to defend first.
- **co-03 · sql-injection-and-parameterized-queries** — concatenating untrusted input into SQL lets an attacker rewrite the query; bound parameters send data and code separately so input can never become SQL.
- **co-04 · command-injection** — passing untrusted input to a shell (`os.system`, `shell=True`) lets it inject commands; `subprocess.run([...], shell=False)` with an argv list removes the shell.
- **co-05 · path-traversal** — `../` sequences in a filename escape the intended directory; canonicalizing (`realpath`) and enforcing a root prefix contains it.
- **co-06 · xss-and-output-encoding** — untrusted data rendered into a page executes as script unless encoded for its exact output context (HTML body, attribute, JS string, URL).
- **co-07 · allow-list-vs-deny-list-validation** — validating against a list of known-good values is robust; blocklists of known-bad inputs always miss the case you didn't foresee.
- **co-08 · mass-assignment-and-over-posting** — binding a whole request body onto a model (`Model(**json)`) lets a client set fields it shouldn't (e.g. `is_admin`); an explicit field allow-list stops it.
- **co-09 · password-hashing-argon2id-bcrypt** — store passwords only as slow, salted one-way hashes (argon2id or bcrypt) — never plaintext, MD5, or SHA-1.
- **co-10 · salting-and-why** — a unique per-hash salt makes identical passwords hash differently and defeats precomputed (rainbow-table) attacks; modern hashers salt automatically.
- **co-11 · timing-safe-comparison** — comparing secrets with `==` leaks length/prefix via timing; `hmac.compare_digest` compares in constant time.
- **co-12 · session-vs-token-auth** — server-side sessions (revocable, stateful) versus stateless tokens (scalable, hard to revoke) are a deliberate trade-off, not interchangeable defaults.
- **co-13 · secure-cookie-flags** — `Secure`, `HttpOnly`, and `SameSite` on session cookies stop transport leakage, JS theft, and cross-site sending respectively.
- **co-14 · jwt-specific-pitfalls** — JWTs fail open on `alg:none`, algorithm confusion (HS256/RS256), and unvalidated `exp`/`aud`/`iss`; pin the algorithm and validate every claim.
- **co-15 · authentication-vs-authorization** — authentication proves _who_ you are; authorization decides _what_ you may do — they are separate checks and both are required.
- **co-16 · least-privilege-access-control** — every user, process, and DB account gets only the access it needs, so a compromise's blast radius is bounded (IDOR/function-level checks, restricted DB roles).
- **co-17 · secret-hygiene** — secrets live in the environment or a manager, never in code or git history; leaked secrets are rotated, and `.env` is gitignored while `.env.example` holds placeholders.
- **co-18 · https-tls-in-practice** — TLS protects data in transit only when certificates are actually verified; disabling verification (`verify=False`) reopens MITM.
- **co-19 · security-headers** — `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, and `X-Frame-Options`/`frame-ancestors` are cheap, high-leverage browser-enforced defenses.
- **co-20 · cors-configuration** — CORS relaxes the same-origin policy; reflecting the request Origin with credentials lets any site read responses — allow-list origins instead.
- **co-21 · dependency-safety-supply-chain** — third-party code is attack surface; pin exact versions, audit with `pip-audit`, watch for typosquats, and keep the tree CVE-clean (DD-23).
- **co-22 · security-logging-and-alerting** — log authn/authz decisions (who, what, outcome — never secrets) and alert on anomalies like brute-force bursts so attacks are visible.
- **co-23 · safe-error-handling** — error responses reveal nothing internal (no stack traces, no SQL); the detail goes to a server-side log, the client gets a generic message.
- **co-24 · security-misconfiguration** — insecure defaults (debug mode, directory listing, default creds, verbose errors) are vulnerabilities; hardening the configuration closes them.
- **co-25 · insecure-design** — some flaws are in the design, not the code: a correctly-implemented flow (unlimited coupon reuse, missing SSRF guard) can still be exploitable — threat-model the feature.
- **co-26 · csrf-protection** — a state-changing request riding the victim's ambient cookie is forgeable cross-site; anti-CSRF tokens and `SameSite` cookies bind the request to your site.
- **co-27 · rate-limiting-and-brute-force-protection** — throttling and backoff on auth endpoints defeat credential-stuffing/brute-force, weighed against lockout-as-DoS.
- **co-28 · open-redirect** — following a user-supplied `next=`/redirect target blindly sends victims to attacker sites; validate against an allow-list or accept relative paths only.

## Worked examples

Colocated under `security-essentials/learning/code/`; each attack + fix is runnable against the
Backend-Essentials app with `curl` (DD-20/DD-30), fully type-annotated Python (DD-39). Contiguous
`ex-01..ex-80`; every example cites the `co-NN` it exercises.

- **ex-01 · trust-boundary-map-tainted-input** — map where untrusted data enters a handler (query, form, header, cookie) and mark each as tainted — verify the reader lists every entry point and which are attacker-controlled. (co-01)
- **ex-02 · owasp-top-10-mapping-exercise** — map 5 seeded bugs in a sample app to their OWASP 2025 categories — verify each bug is tagged with the correct A0N id. (co-02)
- **ex-03 · sql-injection-live-exploit** — `' OR '1'='1` against a naive f-string login query — verify the attacker logs in with no valid password. (co-03, co-01)
- **ex-04 · sql-injection-parameterized-fix** — replace the f-string with bound placeholders (`?`/`%s`) — verify the same payload is now treated as a literal and fails. (co-03)
- **ex-05 · sql-injection-union-data-exfil** — `UNION SELECT` through a search endpoint to read another table — verify it leaks rows, then parameterization blocks it. (co-03)
- **ex-06 · command-injection-live** — a `;`-chained payload through `os.system("ping " + host)` — verify the injected command runs, then `subprocess.run([...], shell=False)` blocks it. (co-04, co-01)
- **ex-07 · path-traversal-file-read** — `../../etc/passwd` through a naive download handler — verify it reads an out-of-root file, then `realpath` + prefix check blocks it. (co-05, co-01)
- **ex-08 · reflected-xss-live** — a `<script>` echoed into an unescaped response — verify it executes, then autoescaping/`markupsafe.escape` neutralizes it. (co-06, co-01)
- **ex-09 · stored-xss-live** — a persisted comment with a script rendered to other users — verify it fires on view, then output-encoding on render stops it. (co-06)
- **ex-10 · output-encoding-by-context** — encode the same value for HTML-body, HTML-attribute, and JS-string contexts — verify each uses the correct encoder and a context mismatch still leaks. (co-06)
- **ex-11 · allow-list-vs-deny-list** — validate a country code against an allow-list vs a bad-char blocklist — verify the allow-list rejects an input the blocklist misses. (co-07)
- **ex-12 · input-validation-at-the-boundary** — a pydantic model validating type/range/format at the edge — verify malformed JSON yields a structured 422 before business logic runs. (co-07, co-01)
- **ex-13 · plaintext-password-store-is-broken** — a login table storing plaintext, dumped via a read — verify every password is visible in the dump. (co-09)
- **ex-14 · md5-password-store-is-broken** — unsalted MD5 hashes cracked with a small dictionary — verify common passwords are recovered in seconds. (co-09, co-10)
- **ex-15 · argon2id-hash-and-verify** — hash with argon2id (m=19456,t=2,p=1) and verify — verify the stored value is a `$argon2id$` PHC string, verify() accepts the right password and rejects a wrong one. (co-09)
- **ex-16 · bcrypt-hash-and-verify** — bcrypt at work-factor 12, noting the 72-byte limit — verify the hash embeds the cost and a truncation demo shows the 72-byte cap. (co-09)
- **ex-17 · salt-makes-identical-passwords-differ** — hash the same password twice with argon2id — verify the two stored hashes differ (per-hash salt). (co-10)
- **ex-18 · timing-safe-token-compare** — compare an API token with `==` vs `hmac.compare_digest` — verify the reader explains the timing side-channel `==` leaks. (co-11)
- **ex-19 · secure-cookie-flags** — set a session cookie `Secure; HttpOnly; SameSite=Lax` — verify `curl -I` shows all three flags and JS `document.cookie` cannot read it. (co-13)
- **ex-20 · secret-in-env-not-code** — move a hardcoded API key to `os.environ` — verify no secret in the source and the app still authenticates. (co-17)
- **ex-21 · gitignore-and-env-example** — `.env` gitignored, `.env.example` committed with placeholders — verify `git status` never lists `.env` and the example holds no real value. (co-17)
- **ex-22 · security-headers-baseline** — add CSP, `X-Content-Type-Options`, `Strict-Transport-Security` — verify `curl -I` shows each header present. (co-19)
- **ex-23 · pip-audit-first-run** — `pip-audit` on a requirements set with one known-vuln pin — verify it reports the CVE and the fixed version. (co-21)
- **ex-24 · pin-and-remediate-a-cve** — bump the flagged dependency to the CVE-clean version, re-audit — verify `pip-audit` exits clean. (co-21)
- **ex-25 · safe-error-message** — replace a stack-trace-leaking 500 with a generic message + server-side log — verify the client sees no internal detail and the log has the trace. (co-23, co-22)
- **ex-26 · second-order-sql-injection** — a payload stored then later concatenated into a query — verify it fires on the second use, then parameterizing both paths blocks it. (co-03)
- **ex-27 · orm-raw-fragment-injection** — an ORM `text()`/`.raw()` fragment built by concatenation — verify it injects, then bound parameters via the ORM fix it. (co-03, co-21)
- **ex-28 · blind-boolean-sql-injection** — infer a value from true/false response differences — verify the reader extracts one character, then the fix removes the oracle. (co-03)
- **ex-29 · argument-injection-not-just-shell** — `--`-style flag injection into a CLI call even with `shell=False` — verify an unexpected flag changes behavior, then an arg allow-list blocks it. (co-04, co-07)
- **ex-30 · dom-based-xss** — a client sink `innerHTML = location.hash` — verify the payload executes purely client-side, then `textContent`/a sanitizer fixes it. (co-06)
- **ex-31 · csp-blocks-inline-script** — a strict nonce-based CSP vs an inline `<script>` — verify the inline script is blocked and the nonce'd one runs. (co-19, co-06)
- **ex-32 · mass-assignment-privilege-escalation** — a `User(**request.json)` bind lets a client set `is_admin=true` — verify the escalation, then a field allow-list blocks it. (co-08, co-07)
- **ex-33 · idor-broken-object-access** — `GET /orders/{id}` returns another user's order — verify the cross-user read, then an ownership check fixes it. (co-15, co-16)
- **ex-34 · missing-function-level-authorization** — an admin endpoint reachable by a normal user — verify access, then a role check returns 403. (co-15, co-16)
- **ex-35 · authn-vs-authz-separation** — a logged-in but unauthorized user hitting a resource — verify the code checks identity and permission separately. (co-15)
- **ex-36 · session-fixation** — reuse a pre-login session id — verify the fixation works, then regenerating the session id on login fixes it. (co-12)
- **ex-37 · session-vs-token-tradeoffs** — implement both a server session and a stateless token for one login — verify each authenticates and the reader states one trade-off (revocation vs scale). (co-12, co-14)
- **ex-38 · jwt-alg-none-attack** — a verifier accepting `alg:none` — verify a forged unsigned token is accepted, then pinning the algorithm rejects it. (co-14)
- **ex-39 · jwt-hs256-rs256-confusion** — signing with the RSA public key as an HMAC secret — verify the confusion forges a token, then binding alg + key type blocks it. (co-14)
- **ex-40 · jwt-expiry-and-claims-validation** — enforce `exp`, `aud`, `iss` on verify — verify an expired or wrong-audience token is rejected. (co-14)
- **ex-41 · csrf-live-exploit** — a cross-site form POST riding the victim's cookie — verify the state-changing request succeeds, then a CSRF token blocks it. (co-26)
- **ex-42 · samesite-cookie-mitigates-csrf** — `SameSite=Strict/Lax` on the session cookie — verify the cross-site POST no longer carries the cookie. (co-26, co-13)
- **ex-43 · cors-misconfig-reflects-origin** — a server echoing `Access-Control-Allow-Origin: <Origin>` with credentials — verify any origin reads the response, then an origin allow-list fixes it. (co-20)
- **ex-44 · cors-preflight-correctness** — a proper preflight for a credentialed cross-origin request — verify the browser allows only the declared methods/headers/origin. (co-20)
- **ex-45 · open-redirect** — `?next=//evil.com` followed blindly after login — verify the redirect leaves the site, then an allow-list/relative-only check fixes it. (co-28)
- **ex-46 · rate-limiting-login** — a per-IP/per-account limiter on login — verify the Nth rapid attempt is throttled (429). (co-27)
- **ex-47 · account-lockout-vs-throttle** — exponential backoff vs hard lockout, with the lockout-as-DoS trade-off — verify brute force slows and the reader names the DoS risk. (co-27)
- **ex-48 · constant-time-login-response** — equal timing/response for unknown-user vs wrong-password — verify a timing/response diff no longer reveals which accounts exist. (co-11, co-27)
- **ex-49 · security-misconfig-debug-mode** — Flask `debug=True` exposing the interactive debugger in prod — verify the console is reachable, then disabling debug closes it. (co-24)
- **ex-50 · directory-listing-and-default-creds** — an exposed listing / default admin password — verify both are reachable, then config hardening closes them. (co-24)
- **ex-51 · tls-verify-not-disabled** — a client with `verify=False` accepting any cert — verify a MITM cert is accepted, then enabling verification rejects it. (co-18)
- **ex-52 · hsts-and-redirect-to-https** — force HTTP→HTTPS + `Strict-Transport-Security` — verify an http request upgrades and repeat visits skip http. (co-18, co-19)
- **ex-53 · secret-scanning-pre-commit** — a `detect-secrets`/pre-commit hook catching a staged key — verify the commit is blocked when a secret is present. (co-17, co-21)
- **ex-54 · secret-rotation-drill** — rotate a leaked key and invalidate the old — verify the old key stops working and the new one authenticates. (co-17)
- **ex-55 · dependency-pinning-and-lockfile** — exact pins + a lockfile hash reproduced on a clean install — verify resolved versions are identical and audit-clean. (co-21)
- **ex-56 · supply-chain-typosquat-check** — flag a typosquatted package name before install — verify the reader identifies the malicious lookalike. (co-21, co-25)
- **ex-57 · structured-security-logging** — log authn/authz decisions with user, action, outcome (no secrets) — verify a failed-login event is queryable and contains no password. (co-22)
- **ex-58 · alert-on-brute-force-pattern** — detect N failures in a window and emit an alert — verify the burst triggers exactly one alert. (co-22, co-27)
- **ex-59 · insecure-design-vs-bug** — a business flow exploitable even when coded correctly (unlimited coupon reuse) — verify the reader distinguishes a design flaw from an implementation bug. (co-25)
- **ex-60 · threat-model-a-feature** — a STRIDE-lite pass over one endpoint listing threats + mitigations — verify each threat maps to a concrete control. (co-25, co-02)
- **ex-61 · end-to-end-injection-audit** — sweep an app for every injection sink (SQL, OS, template) and fix each — verify no concatenated-untrusted-input sink remains. (co-03, co-04, co-01)
- **ex-62 · ssti-server-side-template-injection** — user input into a Jinja template string executes — verify code execution, then rendering data as context (not template) blocks it. (co-06, co-25)
- **ex-63 · argon2-parameter-tuning** — measure hash time and tune m/t/p to a ~250ms target on the box — verify the chosen params hit the budget and beat a weaker baseline. (co-09)
- **ex-64 · password-upgrade-on-login** — transparently rehash legacy bcrypt logins to argon2id at next login — verify a legacy user's stored hash upgrades after one successful login. (co-09, co-10)
- **ex-65 · token-revocation-strategy** — a short-lived access token + refresh + revocation list — verify a revoked refresh token can no longer mint access tokens. (co-12, co-14)
- **ex-66 · rbac-vs-abac-authorization** — role-based then attribute-based checks for the same resource — verify an ownership+role rule allows/denies correctly across cases. (co-16, co-15)
- **ex-67 · least-privilege-db-account** — the app connects with a role lacking DDL/DROP — verify a destructive query is denied by the DB even when injected. (co-16, co-03)
- **ex-68 · defense-in-depth-xss** — combine input validation + output encoding + CSP + HttpOnly cookies — verify removing any one layer still leaves the others catching the payload. (co-06, co-19, co-13, co-07)
- **ex-69 · csrf-for-json-and-spa** — a double-submit-token / custom-header strategy for a token-auth SPA — verify a forged cross-site request lacks the header and is rejected. (co-26, co-20)
- **ex-70 · clickjacking-frame-protection** — `X-Frame-Options`/CSP `frame-ancestors` blocking an iframe overlay — verify the page refuses to render in a foreign frame. (co-19, co-25)
- **ex-71 · secure-file-upload** — validate type/size, store outside webroot, randomize names — verify a disguised executable upload is rejected and stored files are non-executable. (co-05, co-07, co-24)
- **ex-72 · ssrf-safe-outbound-fetch** — block an outbound fetch to internal/metadata IPs (169.254.169.254) — verify a request to a private range is denied. (co-01, co-25)
- **ex-73 · rate-limit-distributed** — a Redis-backed limiter correct across multiple app instances — verify the global limit holds when two workers serve the same client. (co-27)
- **ex-74 · audit-log-integrity** — an append-only / hash-chained security log — verify tampering with a past entry is detectable. (co-22)
- **ex-75 · dependency-cve-triage-workflow** — `pip-audit` → assess exploitability → pin or waiver per the CVE-clean policy — verify each finding ends resolved or documented-waived. (co-21, co-25)
- **ex-76 · sbom-and-provenance** — generate a CycloneDX SBOM and check it against advisories — verify every component is enumerated and audit-clean. (co-21)
- **ex-77 · secrets-manager-integration** — fetch a secret at runtime from a vault/manager instead of env — verify the secret never lands in the image/tree and rotates without redeploy. (co-17)
- **ex-78 · harden-the-full-app-transcript** — apply every control to the Backend-Essentials app with a before/after attack transcript — verify each seeded attack flips from success to blocked. (co-01, co-24, co-02)
- **ex-79 · security-regression-test-suite** — encode each fixed vuln as a failing→passing security test — verify every attack has a red-before/green-after test guarding regressions. (co-02, co-23)
- **ex-80 · secure-error-and-logging-review** — a final pass: no stack traces to clients, no secrets in logs, alerts on auth anomalies — verify a fuzz of error paths leaks nothing and logs stay secret-free. (co-23, co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take the Backend-Essentials API and harden it end to end — fix an injectable query, add
  argon2/bcrypt password auth with secure session/token handling, allow-list input validation, secret
  hygiene via env vars, security headers, and a clean `pip-audit` — with a before/after attack transcript.
- **Concepts exercised**: [ ] parameterized queries (injection fix) [ ] argon2/bcrypt password hashing
  [ ] session/token + secure cookie flags [ ] allow-list validation + output encoding [ ] secrets in env,
  not code [ ] security headers [ ] `pip-audit` clean.
- **Ordered steps**:
  1. `.../learning/capstone/code/` — copy the Backend-Essentials app; script an injection attack with
     `curl` that succeeds. Verify the exploit works, then parameterize the query. Verify the exploit fails.
  2. Add argon2/bcrypt-backed registration/login; store only hashes. Verify a login works and the DB holds
     no plaintext.
  3. Add allow-list validation + output encoding + security headers. Verify malformed/hostile inputs are
     rejected and headers are present (`curl -I`).
  4. Move secrets to env vars; run `pip-audit`. Verify no secret is in the tree and `pip-audit` is clean.
- **Acceptance criteria**: every attack in the transcript fails after hardening; passwords are hashed;
  no secret is committed; `pip-audit` exits clean; the app still serves all endpoints.
- **Done bar**: runnable end-to-end (attack transcript flips red→green) + web-verified.

<!-- Inter-topic capstone spec block: this file anchors two milestone bundles -->

## Capstone spec — inter-topic: capstone-first-working-software (Pass-1 boundary)

- **Weight**: `capstone-first-working-software/_index.md` = **275** (section root, after Pass 1 / topic 17). Kind:
  **pass-boundary**, integrating Pass 1 topics 04–17 (build → store → test → secure).
- **Goal**: ship one small but **complete, secure, tested working application** that a reader builds by
  integrating everything in Pass 1: a Python HTTP JSON service (topic 11) over a normalized SQL database
  (topic 10), driven by clean Python (04) with a Bash run/setup script (05), sound data structures (07)
  and an OO domain model (08), a full test suite across the pyramid (15), and the security hardening from
  this topic (17). Networking (12) and the TS/frontend slice (13/14) appear as the client/consumer side.
- **Concepts integrated**: [ ] HTTP JSON API + validation (11) [ ] normalized DB + parameterized DAL (10)
  [ ] domain model / OOP (08) [ ] apt data structures & algorithms (07) [ ] Bash setup/run script (05)
  [ ] pytest + Hypothesis + integration tests (15) [ ] security hardening: hashed auth, injection-safe,
  secrets in env, `pip-audit` clean (17) [ ] a `curl`/HTTP client walkthrough (12).
- **Ordered steps**:
  1. `capstone-first-working-software/code/` — scaffold the service (11) + schema/migrations (10) + a
     `setup.sh` run script (05). Verify `./setup.sh` boots the app and `curl /health` returns 200.
  2. Implement the domain model (08) + core CRUD with parameterized DAL (07/10). Verify `curl` round-trips
     every resource and invalid input yields structured errors.
  3. Add auth (argon2/bcrypt) + input validation + security headers + env secrets (17). Verify the Pass-1
     attack transcript fails and `pip-audit` is clean.
  4. Build the test suite (15): unit (pytest/Vitest where applicable), a Hypothesis property test, and an
     integration test. Verify all green and coverage is generated.
- **Acceptance criteria**: a reader on a clean machine runs `./setup.sh`, exercises every endpoint with
  `curl`, passes the full test suite, and confirms the app is injection-safe with hashed auth and no
  committed secrets — end to end, no hidden setup.
- **Done bar**: runnable end-to-end (clean-machine reproduction) + web-verified.

## Capstone spec — inter-topic: capstone-full-stack-app (cross-cutting)

- **Weight**: `capstone-full-stack-app/_index.md` = **276** (section root, immediately after
  first-working-software). Kind: **cross-cutting**, integrating Frontend (14) + Backend (11) + SQL (10).
- **Goal**: connect a typed **frontend** (topic 14) to the **backend** (11) over **HTTP** (12), persisted
  in **SQL** (10), so the reader sees a full vertical slice: an accessible UI that reads and writes real
  data through a real API into a real database — the "it actually works, top to bottom" moment.
- **Concepts integrated**: [ ] typed UI with loading/error/empty states (14/13) [ ] `fetch` to the API
  over HTTP (12) [ ] backend endpoints + validation (11) [ ] SQL persistence (10) [ ] end-to-end request
  path narrated (12) [ ] a Testing-Library UI test + an API integration test (15).
- **Ordered steps**:
  1. `capstone-full-stack-app/code/backend/` — reuse the hardened service (11/17) with a CORS-safe read
     endpoint. Verify `curl` returns JSON from the DB.
  2. `capstone-full-stack-app/code/frontend/` — a typed UI (14) that fetches and renders the list with
     loading/error/empty states. Verify the UI shows live data and each state is reachable.
  3. Wire a create/update form (14) posting to the API (11). Verify a UI action persists to the DB and the
     list reflects it after refetch.
  4. Add a Testing-Library test for the UI and an integration test for the endpoint (15). Verify both green.
- **Acceptance criteria**: a reader runs the backend + frontend, performs a create/read/update from the UI,
  confirms the change landed in the SQL DB, and both the UI test and API test pass — the whole stack works
  together.
- **Done bar**: runnable end-to-end (full vertical slice) + web-verified.

## Read more

**Books**

- **Security Engineering** — Ross Anderson (3rd ed., 2020, free from the author). Canonical systems-level treatment of building secure, dependable systems.
- **The Web Application Hacker's Handbook** — Stuttard, Pinto (2nd ed., 2011). Standard practitioner's guide to finding and exploiting web vulnerabilities.

**Papers & articles**

- **OWASP Top 10:2025** — OWASP Foundation (finalized Jan 2026). Consensus list of the most critical web-app security risks. <https://owasp.org/Top10/2025/en/>
- **OWASP Password Storage Cheat Sheet** — OWASP Foundation (continuously updated). Current guidance on password hashing (Argon2id, bcrypt, scrypt) and secrets. <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>

---

← Previous: [16 · Debugging & Profiling](./16-debugging-and-profiling.md) · Next: [18 · Technical Communication](./18-technical-communication.md) →
