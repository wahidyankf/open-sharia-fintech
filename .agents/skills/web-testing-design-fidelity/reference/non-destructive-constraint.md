# Non-Destructive Constraint (Hard Rule)

This agent performs **passive, observational evaluation only** — the discipline OWASP's Web Security
Testing Guide calls _passive testing_: understanding the application without attacking it.

- ALLOWED: navigating, clicking, filling forms with benign synthetic data, resizing viewports, reading
  rendered content / computed styles / console / network, taking screenshots, observing redirects and
  URL structure, reading `robots.txt`/`sitemap.xml` for the IA picture.
- FORBIDDEN: injection, fuzzing, brute-force, load/DoS, scraping at volume, altering or deleting other
  users' data, bypassing auth, or any request crafted to exploit rather than observe. A destructive
  action (delete, purchase, irreversible state change) requires explicit per-run authorization; absent
  it, stop at the confirmation step and record the flow as "not exercised — destructive".
- Never submit real secrets or PII; use obviously-synthetic data. Never record real credentials or
  tokens in the plan (repo no-secrets rule).
