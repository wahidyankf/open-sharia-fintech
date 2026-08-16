# Defect Report Anatomy and Severity/Priority Scales

Every finding in `findings.md` carries the ISTQB-aligned fields:

- **ID** — `AET-001`, `AET-002`, … (stable within the plan).
- **Title** — observed symptom, specific, not the suspected cause
  (e.g. "POST /activities returns 200 with empty body when required `name` is missing").
- **Severity** (technical impact — set here) and **Priority** (business urgency — proposed, owner
  confirms). See scales below.
- **Operation / Component** — the path + method (REST) or query/mutation field (GraphQL), and the
  area.
- **Environment** — base URL, build/commit if exposed, protocol, auth context (synthetic/none), date
  observed.
- **Steps to Reproduce** — the exact `curl` command or GraphQL operation + variables (with secrets
  **redacted**), numbered, minimal, deterministic; include preconditions (e.g. a seeded resource ID).
- **Expected Result** — per contract/spec (cite the OpenAPI clause, SDL type, or `.feature` scenario).
- **Actual Result** — the observed status, headers, and body; quote exact error text verbatim.
- **Evidence** — request/response capture path in the plan's `evidence/` subfolder
  (`./evidence/phase-N-<operation>-<condition>.http`), with `Authorization` and any token redacted —
  never secrets/PII. Captures a finding cites are committed to `evidence/`, not left in `local-tmp/`,
  per the
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
- **Reproducibility** — Always / Intermittent (N/M) / Once.
- **Defect type** — Contract / Functional / Status-code / Error-envelope / Auth / Consistency /
  Pagination / Performance / Security / GraphQL-schema.
- **Suggested fix locus** — best-guess handler/file/area to orient the dev (clearly marked as a
  hypothesis).

## Severity scale (technical impact — tester sets)

| Severity | Meaning                                           | API example                                            |
| -------- | ------------------------------------------------- | ------------------------------------------------------ |
| Blocker  | Core operation completely unusable; no workaround | `POST /activities` returns 500 for every valid body    |
| Critical | Core operation broken or insecure                 | Unauthenticated request reads another account's record |
| Major    | Important operation wrong/inconsistent            | One list endpoint ignores pagination; returns all rows |
| Minor    | Contract/UX degraded, function intact             | `400` returns a different error-envelope shape         |
| Trivial  | Cosmetic; no functional/security impact           | Inconsistent casing in an error `message` string       |

## Priority scale (business urgency — proposed; owner confirms)

| Priority | Meaning                                      |
| -------- | -------------------------------------------- |
| High     | Fix this release; blocks launch/SLA/security |
| Medium   | Fix soon; next planned sprint                |
| Low      | Fix when time allows                         |

Severity ≠ priority — a trivial error-message typo before a public launch can be High priority; a
critical flaw in a zero-traffic internal route can be Low. Record both independently.
