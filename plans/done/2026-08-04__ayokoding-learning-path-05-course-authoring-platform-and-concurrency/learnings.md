<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: ayokoding-learning-path-05-course-authoring-platform-and-concurrency

## Rule-15 three-tester retest exemption — routed inline

- **Context**: Phase 4 requires the exemption to be recorded separately from the manual course-page
  verification.
- **Observation**: This content-only plan ships Markdown bundles, not the navigation UI that renders
  them; dedicated content checkers cover the authored surface; and a generic UI triad would exercise
  the navigation layer owned by
  [`ayokoding-learning-path-03-navigation-ui`](../../done/2026-07-25__ayokoding-learning-path-03-navigation-ui/README.md).
- **Litmus and routing**: The durable, checkable rule already lives in
  [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded), so this entry is
  routed inline to that authoritative record. Manual Playwright verification remains mandatory.
- **Secret/sensitivity gate**: passed; this entry contains no credentials, personal data, or internal
  infrastructure details.
- **Repo-relevance gate**: passed; it applies only to this public repository's content-only plan and
  names the repository-local owner of the waived triad.
- **Terminal state**: routed inline; no further durable edit is needed.

No other generalizable learnings — the remaining execution observations are either current-plan
validation outcomes or ephemeral local-environment conditions and would not make a durable surface
catch a future issue automatically.
