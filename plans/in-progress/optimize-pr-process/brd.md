# Business Requirements: Optimize the Pull Request Process

## Goal and Rationale

Improve review quality without turning delivery into ceremony. Industry guidance favors small,
self-contained changes, descriptions that explain why and how to review, and comments that are
specific, respectful, and educational. Native GitHub conversations preserve that context for later
readers. [Web-cited] Evidence is mapped in
[README.md](./README.md#evidence-labels-and-sources); BR-1–BR-10 are user-ratified `[Judgment call]`
contracts, not measured outcomes.

## Requirements

- **BR-1 — Human-readable PRs:** one cohesive outcome, plain-language context, deliberate reading
  order, review focus, verification, risk, integration safety, rollback, and concise non-goals.
- **BR-2 — Educational review:** findings explain impact, evidence, and a bounded remedy in language
  understandable to a coding-bootcamp graduate; optional teaching never masquerades as a blocker.
- **BR-3 — Critical fixing:** every unresolved finding receives one four-way disposition and a
  same-thread reply; valid pushback is expected, not treated as disobedience.
- **BR-4 — Bounded convergence:** prepare thoroughly for Cycle 1, batch verified fixes, target
  Cycles 1–3, recover autonomously through Cycle 5, and hard-stop before Cycle 6.
- **BR-5 — PR-native auditability:** bodies, reviews, replies, commits, checks, resolutions,
  obligations, deviations, and supersession links must make the process reconstructable.
- **BR-6 — Scope control:** review fixes address the cited defect class only; adjacent work becomes
  a linked follow-up. A review cycle never silently expands the PR.
- **BR-7 — Minimal machinery:** use prose and current GitHub/repository capabilities unless a
  measured gap proves a new mechanism necessary and cheaper than its maintenance burden.
- **BR-8 — Cross-repo coherence:** public portable rules propagate through the canonical workflow;
  private adapts from exact merged pins and records semantic correspondence or deviation.
- **BR-9 — Large-plan safety:** plan docs, rules, bindings, code, tests, ideas, and closure become
  sequential delivery units in one worktree per repo, with a stable `main` between units.
- **BR-10 — Trunk safety:** every multi-PR sequence names its lightest-fit “feature flag,” dependency,
  stable-main proof, and reverse-DAG rollback.

## Success and Non-Goals

Success means humans can understand each PR quickly, junior readers learn from reviews, ordinary
work converges within three cycles, no review-driven scope creep occurs, and both repos end coherent
on `origin/main`. This plan does not optimize for fewer comments, automatic agreement, maximum PR
throughput, or new enforcement infrastructure by default.
