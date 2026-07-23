# Worktree-to-PR Hardening — Decompose the Monolithic PR Reviewer

> **Status**: In Progress. Authored in a **non-interactive** session; all design decisions D1–D15 are
> now resolved (see [tech-docs.md §Grilling Deferred — Decisions for Maintainer](./tech-docs.md#grilling-deferred--decisions-for-maintainer)).
> The plan passed the strict plan-quality-gate before promotion. Delivery Mode `worktree-to-pr` —
> delivered in a worktree through a draft PR, gated by the very Maker→Fixer Cycle whose reviewer half
> it redesigns.

## Context

This repo's default delivery mode is `worktree-to-pr` [Repo-grounded]: every plan works in its own
worktree, opens a draft PR, and passes the **PR-Review Maker→Fixer Cycle** (a fixed 3-cycle
`pr-review-maker` → `pr-review-fixer` loop, CI-gated between cycles) before an `[AI]` merge. Today
the review half of that loop is a **single monolithic agent**, `pr-review-maker.md`
[Repo-grounded — 225 lines], that judges correctness bugs, safety, scope-creep, CI-gaming/test
integrity, security, and convention conformance all in one pass.

A single reviewer carrying six distinct review disciplines has a structural weakness: each
discipline draws on a different body of practice (architecture tradeoff analysis vs. domain-logic
conformance vs. mechanical rule-conformance), and one agent holding all of them tends to over-weight
whichever bucket is easiest to pattern-match and under-explore the rest. This plan hardens the
`worktree-to-pr` workflow, with its **centerpiece** being the decomposition of `pr-review-maker`
into a set of focused, non-overlapping specialized reviewer agents plus a **mandatory
coordinator/synthesizer** that deduplicates, re-categorizes, reasonableness-filters, and
tool-verifies before producing the single consolidated review that feeds `pr-review-fixer`.

**This is a design/planning deliverable that ships agent-definition and governance documents — it
does not implement application code.** The plan itself declares Delivery Mode `worktree-to-pr`, so
it **dogfoods the very workflow it improves**.

## Repo Scope — Three-Repo Parity Deliverable

Everything this plan changes — the new PR-review agents, the `pr-review-synthesis-maker` coordinator,
the `pr-review-quality-gate` workflow revision, the reviewer-discipline convention, and the
`pr-merge-protocol.md` changes — is part of the **shared scaffolding
layer** (governance / AI agents / conventions / CI harness) that stays in **parity** across all three
sibling repos, exactly like the prior `standardize-repo-toolchain-parity` and `lint-safety-parity`
3-repo plans [Repo-grounded — AGENTS.md §Related Repositories].

- **`ose-public`** (this repo) is the **source of truth**: every agent/workflow/convention/governance
  change is authored and validated here first.
- **`ose-primer`** is the downstream **public template** (scaffolding layer). It receives the identical
  artifacts after they land in `ose-public`.
- **`ose-infra`** is the **private** infrastructure repo. It also carries the
  `.claude/agents/`, `repo-governance/`, and binding scaffolding this plan changes, and receives the
  identical artifacts.

All three carry the `.claude/agents/`, `repo-governance/`, and OpenCode/Amazon-Q binding scaffolding
this plan touches. Propagation is delivered **in the spirit of** the
[multi-repo parity planning-and-execution workflow](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning-and-execution.md)
(and its planning companion
[plan-multi-repo-parity-planning.md](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)),
**adapted to a single shared plan folder** rather than that workflow's canonical one-folder-per-repo
output — the same single-folder posture the precedent `standardize-repo-toolchain-parity` and
`lint-safety-parity` 3-repo plans used. `ose-public` merges first, then the same change set propagates
to `ose-primer` and `ose-infra`, **each via its own `worktree-to-pr` delivery** (own worktree + PR +
review cycle + merge) with a per-repo binding-emit step. See
[tech-docs.md §Repo Scope & Propagation](./tech-docs.md#repo-scope--propagation-three-repo-parity) for
the bare-repo topology caveat, the rhino-cli byte-identity note, and the single-folder /
archival-timing rationale.

## The Pivotal Constraint (why a coordinator is non-negotiable)

The one peer-reviewed head-to-head found for multi-agent code review — **SWR-Bench** (arXiv
2509.01494, Zeng et al., FSE 2026) [Web-cited — see tech-docs.md] — reports a naive multi-agent
baseline scoring **F1 9.22% vs. a single-pass reviewer's 18.73%**, attributing the regression to
"interaction overhead and error propagation among agents." A naive fan-out _regresses_ review
quality. What makes a production split work is precisely the coordination layer: **Cloudflare**'s
production system (blog.cloudflare.com/ai-code-review, 2026-04-20) [Web-cited] runs 7 concurrent
specialized reviewers **plus a coordinator** that dedups, re-categorizes, reasonableness-filters,
and tool-verifies. The coordinator is therefore a first-class, mandatory part of this design — not
an afterthought.

## Scope

**In scope**:

- Decompose `pr-review-maker` into specialized reviewer-maker agents (proposed set below).
- Add a mandatory `pr-review-synthesis-maker` coordinator agent.
- A new governance convention defining the reviewer disciplines and the **boundary tie-breaker rule**
  that resolves grey-zone findings.
- Revise `pr-review-quality-gate.md` so each cycle fans out to the specialists, synthesizes, then
  hands the consolidated review to the unchanged `pr-review-fixer`; **retire the monolithic
  `pr-review-maker` at cutover** (D2).
- Quality-gate enhancements: confidence-calibration spot-check, selective adversarial verification
  for high-risk diffs, a CRITICAL-requires-reproduction rule, and a documented rationale for the
  3-cycle/no-early-exit policy.
- **Cloudflare-folded cost/noise mechanics** (added 2026-07-23, verified via `web-researcher`):
  risk-tier fan-out that scales agents to diff size (D12), shared-context + large-diff handling
  (D13: no generated-file exclusion), per-specialist `SUPPRESS` blocks, instruction-decay coverage via
  a dedicated `pr-review-instruction-maker` specialist (D14), human-dismissal-respect on re-review, and
  boundary-tag-strip untrusted-input hardening. See [tech-docs.md §Cost-Control & Noise-Control Mechanics](./tech-docs.md#cost-control--noise-control-mechanics-cloudflare-production-learnings--folded-2026-07-23).
- A **post-cutover monitoring plan** (precision, acceptance rate, BitsAI-CR "Outdated Rate") with a
  documented **rollback trigger** that restores the monolith from git history if metrics regress.
- A future-work workstream: the AI-attribution/bot-identity gap, cost/latency budgeting, and the
  **deferred merge queue** (D7/D10 — researched but NOT adopted here; the repo exposes no merge-queue
  branch setting, so it is split into its own backlog plan:
  [`merge-queue-adoption`](../../backlog/merge-queue-adoption/README.md)).
- Register/index/binding updates for every new agent (`AGENTS.md`, `.claude/agents/README.md`,
  `npm run generate:bindings`).

**Out of scope**:

- Implementing any application code under `apps/` or `libs/`.
- Provisioning a dedicated GitHub App / bot identity (tracked separately in
  [`plans/ideas/pr-review-bot-identity.md`](../../ideas/pr-review-bot-identity.md) [Repo-grounded]).
- Changing `pr-review-fixer`'s core triage contract (it keeps consuming a consolidated finding set;
  whether to split it too is a deferred decision).

## Proposed Agent Set (refine via the deferred decisions)

| Agent                          | Discipline                     | Charter (one line)                                                                      |
| ------------------------------ | ------------------------------ | --------------------------------------------------------------------------------------- |
| `pr-review-architecture-maker` | Architecture / design          | Is this a sound _new_ tradeoff? Reversibility, blast radius, quality-attributes         |
| `pr-review-logic-maker`        | Business-logic / correctness   | Does behavior match domain intent + Gherkin acceptance criteria across edges            |
| `pr-review-governance-maker`   | Convention / rules-conformance | Does the diff mechanically conform to an already-documented `repo-governance/` rule     |
| `pr-review-security-maker`     | Security                       | Secrets, injection, untrusted-input, git-fixture isolation, unsafe operations           |
| `pr-review-integrity-maker`    | CI-gaming / test integrity     | Weakened/skipped tests, missing regression tests, coverage-gaming                       |
| `pr-review-performance-maker`  | Performance                    | Concrete/likely regressions, hot paths, algorithmic complexity, resource use            |
| `pr-review-docs-maker`         | Documentation quality          | README/docs/Diátaxis conformance, doc drift, completeness/clarity, doc alt-text/a11y    |
| `pr-review-instruction-maker`  | Instruction decay              | Framework/CI/env change not reflected in AGENTS.md/CLAUDE.md/.claude; instruction bloat |
| `pr-review-synthesis-maker`    | **Coordinator (mandatory)**    | Dedup + re-categorize + reasonableness-filter + tool-verify → one consolidated review   |

The maintainer chose the **7-specialist** set (D1): performance and docs-quality are their own agents,
not folded — meaningful here because this repo is content/markdown-heavy (docs) and has real hot-path
code in its polyglot CLIs/backends (performance). **D14 then added an eighth specialist,
`pr-review-instruction-maker`** (instruction-decay), so the set is now **8 specialists + the
coordinator**. The non-overlap boundaries that keep them out of architecture and governance are in
[tech-docs.md §Agent Charters](./tech-docs.md#agent-charters-non-overlapping).

## Navigation

- [brd.md](./brd.md) — WHY: business rationale, impact, risks, success metrics.
- [prd.md](./prd.md) — WHAT: personas, user stories, Gherkin acceptance criteria, product scope.
- [tech-docs.md](./tech-docs.md) — HOW: architecture, agent charters, the boundary tie-breaker, the
  research grounding, diagrams, and the **Grilling Deferred — Decisions for Maintainer** section.
- [delivery.md](./delivery.md) — DO: phased, gated delivery checklist (Delivery Mode
  `worktree-to-pr`).
- [learnings.md](./learnings.md) — Knowledge Capture running log.

## Delivery Mode

`worktree-to-pr` (the repo default). This plan dogfoods the workflow it hardens: it is delivered in a
worktree, through a draft PR, gated by the very Maker→Fixer Cycle whose reviewer half it redesigns.
