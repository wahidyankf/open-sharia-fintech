<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: ayokoding-www-ai-benchmark-merged-chart

## Learning: stuck self-hosted-runner step has no documented diagnostic/remediation

- **Context**: Phase 7 CI run 30548513998's "Detect affected languages" job's `setup-node` step
  stalled ~10 min with zero progress (unchanged `startedAt` across polls) while every sibling job's
  equivalent step completed in seconds, cascading 4 dependent jobs to `cancelled`.
- **Observation**: `ci-monitoring.md` and `ci-blocker-resolution.md` both reference shared
  self-hosted-runner contention (the latter explicitly excludes "runner disk full" etc. from its
  scope as an operational, not code, issue) but neither documented HOW to diagnose a stuck step
  (compare step-level `startedAt` across polls) or the surgical remediation
  (`gh run cancel` + `gh run rerun --failed`, which preserves already-passed jobs).
- **Why it might generalize**: this class of incident (a job silently hanging with zero progress on
  a shared runner) recurs — a documented diagnostic saves the next agent from either waiting
  indefinitely or over-cancelling a whole run.

**Routing**: `repo-governance/development/workflow/ci-monitoring.md` (non-code, small) — routed
INLINE, new "Diagnosing a Stuck Self-Hosted Runner Job" subsection landed in this plan's Phase 8
commit.

## Learning: DWT-004's root cause was two values deriving from one shared constant

- **Context**: the band-header/row-label overlap defect (DWT-004) traced to `headerY` and the
  first row's own `y` both deriving via fixed subtraction from the SAME `BAND_HEADER_HEIGHT`
  constant, so they moved in lockstep and never visibly diverged even though they measured
  conceptually different things.
- **Observation**: this is a specific instance of general root-cause debugging (already covered by
  the [Root Cause Orientation principle](../../../repo-governance/principles/general/root-cause-orientation.md)
  and the "trace to root cause" step in `ci-blocker-resolution.md`) applied to this one component's
  SVG layout math, not a new class of defect a static checker could reliably detect (a legitimate
  shared constant is common and correct in most layout code; only this specific coupling was a bug).
- **Litmus**: no durable surface would change behavior by routing this further — the existing
  Root Cause Orientation principle already covers the general debugging discipline that found it,
  and encoding "never derive two independent values from one constant" as a checker rule would
  produce false positives on legitimate shared-constant layout code.

**Routing**: discard — not generalizable beyond the existing Root Cause Orientation principle;
no new rule proposed to avoid false-positiving legitimate shared-constant layout code.

## Learning: AskUserQuestion for a fix that conflicts with an already-reviewed design decision

- **Context**: UWT-001's obvious full fix (bars + sort for the Unrated band) would have reopened
  DD-1, an already-reviewed design decision in `tech-docs.md` that deliberately renders
  subscription-only/unrated models as plain text, not bars. Used `AskUserQuestion` to get an
  explicit user disposition (partial fix: price info only, no bars/sort) instead of silently
  picking one side.
- **Observation**: `user-facing-delivery-hardening.md` Rule 15 already requires "explicit user
  permission" when a rule-15 finding's fix is deferred or genuinely impossible; this instance
  extends that same explicit-permission pattern to a finding whose straightforward fix would
  reopen prior design decision rather than being merely deferred.
- **Litmus**: the underlying principle (explicit user permission before overriding/reopening a
  prior design decision) is already stated in Rule 15's deferral clause; this is an application of
  that existing rule to a slightly different trigger (design conflict, not impossibility), not a
  gap in the rule's wording.

**Routing**: discard — already covered by `user-facing-delivery-hardening.md` Rule 15's existing
explicit-user-permission requirement; no wording gap found.
