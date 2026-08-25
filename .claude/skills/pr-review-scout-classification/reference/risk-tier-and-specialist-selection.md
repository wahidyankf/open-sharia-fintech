# Risk-Tier Classification + Specialist-Set Selection (D12)

Classify the PR into exactly one risk tier by line count, file count, and whether it touches a
security-sensitive path, then select the specialist set accordingly:

- **Trivial, standard non-plans-only route** (≤10 changed lines AND ≤20 files, no
  security-sensitive path) → **zero
  specialists**: hand the assembled context brief to `pr-review-synthesis-maker`, which performs
  one consolidated generalist pass itself, with no specialist fan-out at all (see the Trivial-Tier
  Handoff in
  [untrusted-input-and-output-contract.md](./untrusted-input-and-output-contract.md)).
- **Lite** (≤50 lines AND ≤20 files) → the **five highest-yield specialists** for this repo
  (`pr-review-governance-maker`, `pr-review-architecture-maker`, `pr-review-logic-maker`,
  `pr-review-security-maker`, `pr-review-integrity-maker`). `pr-review-types-maker` is
  `full`-tier-only; promotion to `lite` is gated on acceptance-rate data.
- **Full** (>50 lines OR >20 files OR touches a security-sensitive path — secrets/`.env`, git
  identity, CI/workflow files, `pr-merge-protocol.md`) → **all nine specialists, minus the
  Content-Type Applicability Filter below**.

## Plans-Only Route

For a PR whose entire hand-authored diff is plan documents and required indexes, apply the fixed
[Plans-Only Route](./plans-only-route.md). Recompute it every cycle and record the ordinary risk
tier, but emit and use the linked route-selected specialist set and primary probe regardless of
that tier.

**Security-sensitive paths force `full` regardless of size for every non-plans-only PR** —
non-negotiable, per the no-secrets and git-identity rules. Recompute the tier and route **every
cycle**, since the fixer's commits can change the diff's size, touched paths, or content type, and
record both in the shared-context brief so `pr-review-synthesis-maker` carries the decision into
the Consolidated Review Header.

The scout records the resulting tier, route, and every selected or skipped specialist in the PR's
human-readable review-route record. A selected lens names its risk; a skipped lens names its tier
or filter reason.

## Content-Type Applicability Filter (DD-10) — `full` tier only, freshly re-derived every cycle

Two specialists' own charters declare themselves gated on a specific artifact class existing in
the diff rather than applying to any changed file. Skip a specialist from this cycle's
fan-out **only** when its own declared artifact class is verifiably absent from **this cycle's
current diff** — never from a prior cycle's diff, never cached:

- `pr-review-types-maker` — skip if the current diff contains **zero** files with a
  TypeScript/Rust/F#/C# extension (`.ts`, `.tsx`, `.rs`, `.fs`, `.fsx`, `.cs`) or this repo's own
  equivalent typed-language set.
- `pr-review-integrity-maker` — skip if the current diff contains **zero** test files or
  CI/workflow config files (this repo's own test-path and `.github/workflows/**` conventions).

The other seven specialists are never skipped by this filter; include a specialist when
applicability is ambiguous.

Because the diff's file-type composition can change between cycles (a fixer's pushed fix might add
a test file absent in cycle 1), this filter is **re-applied from a fresh reading of the current
diff every cycle** — a specialist skipped in cycle 1 is
not permanently excluded; re-evaluate it fresh in cycle 2 and cycle 3 exactly as the tier itself
is re-evaluated fresh each cycle, per the `fresh pr-review-scout-maker(...)` instantiation in the
workflow's Loop Algorithm.
