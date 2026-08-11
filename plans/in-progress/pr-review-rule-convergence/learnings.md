# Learnings: PR Review Rule Convergence

<!-- Append sanitized, generalizable convergence observations during execution. -->
<!-- Never record secret values, matching fragments, private paths, or hosting-provider case details. -->
<!-- Before archival, triage every entry to an existing/new plans/ideas two-pager or record none. -->

## File-Touch Ledger

- `plans/in-progress/pr-review-rule-convergence/learnings.md` — P0-001 baseline and execution notes.
- `plans/in-progress/pr-review-rule-convergence/delivery.md` — P0 task status and evidence.
- `repo-governance/workflows/pr/pr-review-quality-gate.md` — P1-001 through P1-004A canonical
  behavior classifier, bounded review, and convergence policy.
- `repo-governance/development/workflow/pr-merge-protocol.md` — P1-005 route-specific merge
  preconditions and universal secret stop.
- `repo-governance/development/quality/pr-review-disciplines.md` — P1-006 eligible specialist
  scope, code-related severity disposition, and seven-cycle convergence alignment.
- `repo-governance/development/workflow/git-push-safety.md` — P1-007 limited lease-protected
  exception for secret remediation.
- `repo-governance/conventions/security/secrets-and-env-standards.md` — P1-007 authoritative
  containment, all-reachable-ref rewrite, replacement-PR, and provider-purge procedure.
- `repo-governance/development/workflow/ci-monitoring.md` — P1-007A active-goal preservation
  during shared runner contention.
- `repo-governance/development/workflow/worktree-and-artifact-cleanup.md` — P1-007B exact-path,
  self-created worktree cleanup without a prompt.
- `repo-governance/conventions/structure/plans.md` — P1-007B AI cleanup checklist rule.
- `repo-governance/workflows/plan/plan-execution.md` — P1-007B terminal cleanup procedure.
- `plans/in-progress/repository-onboarding-readme-refresh/delivery.md` — P1R-015 forward-facing
  replacement of retired fixed-cycle instructions; historical execution records are unchanged.
- `.claude/agents/pr-review-fixer.md` and generated `.cursor/agents/pr-review-fixer.md` plus
  `.opencode/agents/pr-review-fixer.md` — P1R-017 retired-anchor repair and generated propagation.
- `plans/ideas/q2-not-urgent-important/plan-archival-in-pr-multi-repo-gap.md` — P1R-017 live idea
  anchor repair.
- `AGENTS.md`, `docs/reference/related-repositories.md`,
  `repo-governance/conventions/structure/plans.md`, and `.claude/agents/repo-rules-maker.md` — P2
  public entry-point propagation.
- `.claude/agents/plan-maker.md`, `.claude/agents/plan-checker.md`, and
  `.claude/skills/plan-creating-project-plans/SKILL.md` — P2 classifier propagation to future plan
  authoring/checking.
- Generated `.cursor/`, `.opencode/`, and `.amazonq/` binding paths changed by P2 regeneration.

## P0 Canonical Inventory

- Primary algorithm: `repo-governance/workflows/pr/pr-review-quality-gate.md`.
- Merge and delivery consumers: `repo-governance/development/workflow/pr-merge-protocol.md`,
  `repo-governance/conventions/structure/plans.md`, and
  `repo-governance/workflows/plan/plan-execution.md`.
- Cross-cutting consumers: `AGENTS.md`, `repo-governance/development/quality/pr-review-disciplines.md`,
  `repo-governance/development/workflow/ci-monitoring.md`,
  `repo-governance/conventions/security/secrets-and-env-standards.md`,
  `repo-governance/development/workflow/worktree-and-artifact-cleanup.md`,
  `docs/reference/related-repositories.md`, and `.claude/agents/repo-rules-maker.md`.
- Review/plan agent consumers requiring a source-of-truth update: `.claude/agents/plan-maker.md`,
  `.claude/agents/plan-checker.md`, `.claude/agents/plan-execution-checker.md`,
  `.claude/agents/pr-review-scout-maker.md`, and `.claude/agents/pr-review-fixer.md`.
- The Phase 1R live-plan search returned all named AyoKoding backlog plans and
  `repository-onboarding-readme-refresh`; its per-file disposition is recorded during P1R.

## P0 CI Baseline

`pr-quality-gate` is the workflow name. Its top-level jobs are `detect`, `format`, `build-rhino`,
`enumerate`, `gate`, `typescript`, `dotnet`, `rust`, `compat-min-version`, `specs-structure`, and
`quality-gate`. Final verification therefore uses the PR's current-head check set, not a remembered
subset of jobs.

## P0 Idea Disposition

The existing `pr-review-bot-identity` idea concerns reviewer identity, not Low-finding deferral or
cycle-six non-convergence. No existing two-pager owns the future Low-finding capture defined by this
plan; create one only if the execution produces a concrete reusable Low finding or slow-convergence
cause.

## P0 Portable-File Manifest Baseline

The portable manifest covers `AGENTS.md`; the PR-review workflow; merge, discipline, CI-monitoring,
secret, cleanup, plan-structure, and plan-execution rules; the related-repositories reference; and
`.claude/agents/repo-rules-maker.md`. SHA-256 values were captured from the public worktree before
edits and are available from the sanitized command record; private comparison occurs in this plan's
separate worktree without reading the concurrent remediation worktree.

## P1 Review-Route Decision

The behavior classifier is intentionally separate from risk-tier selection: first decide whether a
PR changes executable behavior at all, then use the existing scout tiering only for eligible PRs.
This prevents a docs-only diff from paying for specialist fan-out while ambiguity remains fail-safe
eligible. The cycle ceiling is seven, not a target: an eligible PR exits after the first clean cycle
with no code-related MEDIUM/HIGH/CRITICAL findings; cycles six and seven require sanitized learning
and a deduplicated improvement idea.

## P1 Merge-Protocol Decision

The protocol treats `pr-quality-gate.yml` as the complete special review requirement for a
noneligible PR, while preserving shared safety conditions and making secret handling universal.
Eligible PRs retain route-appropriate local, CI, and behavioral tester requirements.

## P1 Discipline-Scope Decision

Eligibility is decided before risk-tier selection, so discipline prompts cannot accidentally spend
specialist fan-out on a static-only PR. The Low disposition is evidence-preserving but
non-blocking; it must be visible to the coordinator and deduplicated into the idea backlog.

## P1 Secret-Remediation Decision

Secret remediation treats reachability, rather than the visible current file, as the completion
criterion. The procedure allows only incident-scoped `--force-with-lease` pushes and requires a
clean replacement PR; it never records a secret value and cannot erase external clones or caches.

## P1 Runner-Contention Decision

Runner contention is distinct from a failing goal: retain the goal and delivery checklist, poll at
the existing cadence, and investigate cross-repository queue state before attempting a rerun or code
diagnosis.

## P1 Cleanup Decision

Immediate cleanup is safe only when the exact path is recorded as self-created for the plan and is
clean, pushed, and no longer needed. Those checks replace a confirmation prompt; broad paths and
foreign worktrees remain categorically out of scope.

## P1R Retrofit Manifest

- `plans/backlog/ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness/**` —
  `current`: no matching forward-facing retired-policy instruction.
- `plans/backlog/ayokoding-learning-path-07-course-authoring-low-level-systems/learnings.md` —
  `historical-record-exempt`: generic value-sanitization guidance, not a cycle/merge policy.
- `plans/backlog/ayokoding-learning-path-08-course-authoring-security-and-ops/**` — `current`: no
  matching forward-facing retired-policy instruction.
- `plans/backlog/ayokoding-learning-path-09-course-authoring-interview-technique/learnings.md` —
  `historical-record-exempt`: generic value-sanitization guidance, not a cycle/merge policy.
- `plans/backlog/ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/**` through
  `plans/backlog/ayokoding-learning-path-18-skills-erp-enterprise-depth/**` — `current`: no matching
  forward-facing retired-policy instruction.
- `plans/in-progress/repository-onboarding-readme-refresh/delivery.md` — `edit`: future delivery
  route and unchecked P2/P9B/P12 review tasks used a fixed three-cycle instruction.
- `plans/in-progress/repository-onboarding-readme-refresh/artifacts/reader-doc-disposition-ose-public.md`
  — `historical-record-exempt`: append-only reader inventory that links the canonical workflow.
- `plans/in-progress/README.md` and this plan's own documents — `current`: already describe the new
  policy.

The final deterministic re-scan is recorded after the edits, with no secret values or private paths.

## P1R Final Scan

The re-scan found no remaining forward-facing old-cycle or per-plan review rule. The retained matches
are two generic learning-sanitization entries, two historical execution observations in the onboarding
plan, and an append-only reader inventory that references the canonical workflow; each is exempt
because changing it would falsify historical evidence rather than alter future execution.

## P1R Gate Discovery

The Phase 1 link gate found two retired workflow anchors: one in the `pr-review-fixer` source agent
and one in a live idea. This is a forward-facing documentation defect, not a historical-record
exception; repair and generated-binding synchronization are added as P1R-017.

`npm run generate:bindings` propagated the fixer source repair. `npm run validate:sync` still reports
five unrelated pre-existing malformed OpenCode agent files and a transient fixer body-mismatch report
despite a direct source/body comparison being equal; retain this as a later P2 verification finding.
