# Plans-Only Review Route

Treat a PR as plans-only only when its entire hand-authored diff consists of `plans/**` documents
and their required plan indexes. Generated mirrors do not affect the test. Recompute the verdict
from the current diff every cycle.

Record the ordinary risk tier, but select exactly these specialists plus
`pr-review-synthesis-maker` as coordinator regardless of that tier:

- `pr-review-security-maker` — run the primary mandatory probe for real secrets, credentials, or
  other values that grant access, using the canonical
  [system-secret boundary](../../../../repo-governance/conventions/security/secrets-and-env-standards/hard-iron-rule-no-secrets-in-committed-files.md).
- `pr-review-architecture-maker` — review architecture and design decisions made by the plan.
- `pr-review-logic-maker` — review domain intent and Gherkin acceptance-criteria completeness.
- `pr-review-docs-maker` — review the plan as the shipping artifact for substantive quality and
  completeness.
- `pr-review-governance-maker` — review mechanical conformance to repository rules.

Suppress findings that merely complain that eventual implementation artifacts are absent from the
plans-only PR. Later implementation correctness belongs to the PR that ships that implementation;
the plan's own architecture, domain criteria, contradictions, omissions, and rule violations remain
in scope.

Record the plans-only verdict, primary probe, and every selected or skipped specialist in the
human-readable review-route record. For every non-plans-only PR, the standard risk-tier route and
Content-Type Applicability Filter remain in force.
