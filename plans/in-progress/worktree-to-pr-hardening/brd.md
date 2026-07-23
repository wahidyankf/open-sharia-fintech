# Business Requirements — Worktree-to-PR Hardening

## Business Goal

Raise the **signal quality** of the automated PR-review gate that stands between every
`worktree-to-pr` plan and `main` — across all three sibling repos — by replacing one overloaded
reviewer with a set of focused specialists coordinated by a mandatory synthesizer, without regressing
review quality, exploding review cost, or drowning the fixer in low-value findings.

## Repo Scope — Three-Repo Parity

This is a **three-repo parity deliverable**, not an `ose-public`-only change. The PR-review agents,
coordinator, workflow revision, reviewer-discipline convention, and `pr-merge-protocol.md` changes
are all **shared scaffolding** (governance / AI agents / conventions / CI
harness) held in parity across `ose-public`, `ose-primer`, and `ose-infra` — the same posture as the
prior `standardize-repo-toolchain-parity` and `lint-safety-parity` 3-repo plans [Repo-grounded —
AGENTS.md §Related Repositories].

- **`ose-public`** — source of truth; all changes authored and validated here first.
- **`ose-primer`** — downstream public template (scaffolding layer); receives identical artifacts.
- **`ose-infra`** — private infrastructure repo; also carries the `.claude/agents/`,
  `repo-governance/`, and binding scaffolding, and receives identical artifacts.

Propagation to the two downstream repos is delivered **in the spirit of** the
[multi-repo parity planning-and-execution workflow](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning-and-execution.md)
— adapted to this plan's single shared `ose-public` plan folder rather than that workflow's canonical
one-folder-per-repo output (see [tech-docs.md §Repo Scope & Propagation](./tech-docs.md#repo-scope--propagation-three-repo-parity)
for the rationale) — with each downstream repo still delivered via its own `worktree-to-pr` cycle.
Business rationale for the parity posture: the review gate that guards `main` must be **identical** in
every repo, or a PR in one repo merges under a weaker gate than the same change would face in another —
the exact drift the parity loop exists to prevent.

## Business Rationale (why this exists)

The `worktree-to-pr` workflow is the repo's default integration path [Repo-grounded — AGENTS.md
§Delivery Mode]. Its review half is currently a single agent that must simultaneously reason as an
architect, a domain-logic reviewer, a rules auditor, a security reviewer, and a test-integrity
reviewer. These are genuinely distinct disciplines with distinct bodies of practice (documented in
[tech-docs.md](./tech-docs.md#finding-2--three-review-disciplines-are-genuinely-distinct)). A single
agent holding all of them tends to over-report from whichever bucket pattern-matches most cheaply and
under-explore the others — an effect Cloudflare observed even _with_ a split (its Code-Quality
reviewer alone produced 47% of all findings) [Web-cited].

Separating the disciplines lets each specialist apply a sharp, self-consistent charter, and lets the
repo's **large governance surface** (a whole `repo-governance/` tree of mechanically-checkable rules)
get a dedicated rules-conformance reviewer — a dimension most repos do not separate but that is
uniquely valuable here.

The decisive caveat is that a _naive_ split makes things worse, not better (SWR-Bench: F1 9.22% vs.
18.73% single-pass) [Web-cited]. The business value is therefore realized **only** if the
coordinator/synthesizer is built as a first-class component. Per the maintainer's decision (D2), the
monolith is **retired immediately at cutover** when the eight specialists + coordinator land — it is
not gated on an eval. The eval instead runs **post-cutover** as ongoing quality monitoring with a
documented **rollback trigger**: if post-cutover precision/acceptance regress below the rollback bar,
the monolith is restored from git history.

## Business Impact

**Pain points addressed**:

- **Diluted review attention** — one agent covering every discipline at once, uneven coverage. The
  eight specialists give each discipline its own budget and charter.
- **No dedicated governance-conformance lens** — the repo's largest quality surface (its own
  conventions) shares attention with everything else in the monolith.
- **Grey-zone mis-categorization** — architecture-vs-correctness-vs-governance boundary calls are made
  implicitly and inconsistently. A written tie-breaker rule + a coordinator that owns re-categorization
  makes them explicit.

**Expected benefits** (qualitative reasoning — not measured targets):

- Higher **precision** of the consolidated review (the coordinator drops speculative/duplicate/
  convention-contradicted findings before they reach the fixer). _[Judgment call — validated by the
  eval plan in tech-docs.md, not asserted as an achieved number.]_
- Sharper, teachable **charters** that make each reviewer auditable in isolation.
- A **measurable** review gate: precision, acceptance rate, and an "Outdated Rate" adoption metric
  (BitsAI-CR) [Web-cited] that monitors the split post-cutover and drives the rollback trigger.

## Affected Roles (hats the solo maintainer wears; agents that consume these files)

- **Governance author** — writes the new reviewer-discipline convention + tie-breaker rule.
- **Agent author** — scaffolds the specialist + coordinator agent-definition files.
- **Workflow author** — revises `pr-review-quality-gate.md` for the fan-out → synthesize → fixer shape.
- **Consuming agents** — `plan-execution` (invokes the review workflow at finalization),
  `pr-review-fixer` (consumes the consolidated review), the nine new reviewer agents themselves
  (eight specialists + one coordinator), and the binding generators (`.opencode/`, `.amazonq/`) that
  mirror the new agents.

This is a solo-maintainer repo — there is no sign-off ceremony, sponsor, or stakeholder gate. The
maintainer wears each hat above in sequence.

## Business-Level Success Metrics

Gut-based reasoning is used where no measurement exists yet; nothing below is presented as an
already-observed number.

- **Clean cutover with a working rollback path** (observable fact once executed): the monolith is
  removed at cutover and post-cutover monitoring is live, with the rollback trigger documented and the
  monolith restorable from git history if the rollback bar is breached. \_[D6 decided 2026-07-23: an
  absolute-threshold bar needing no pre-cutover monolith baseline — precision < 50% / override-rate
  > 5% / any CRITICAL false-positive — which resolves the D2×D6 baseline contradiction.]\_
- **No unresolved-finding regression** (observable fact): after cutover, a `worktree-to-pr` PR still
  reaches the 5 hardened merge preconditions with 0 CRITICAL + 0 HIGH outstanding, exactly as today.
- **Review cost stays bounded** (observable, tracked): per-PR review cost is budgeted and monitored
  **per risk-tier**, given the fan-out multiplies per-cycle agent invocations but the risk-tier
  mechanism (D12) scales the agent count to diff size — Cloudflare's median ≈ $0.98/review holds
  precisely _because_ most PRs never trigger the full 7-agent fan-out [Web-cited]. See the cost/latency
  and giant-diff risks in [tech-docs.md](./tech-docs.md#risks) and the
  [cost/noise mechanics](./tech-docs.md#cost-control--noise-control-mechanics-cloudflare-production-learnings--folded-2026-07-23).

## Business-Scope Non-Goals

- Not a bid to maximize _raw finding count_ — more findings without more value is an explicit
  anti-goal (the coordinator exists to suppress that).
- Not provisioning a bot/GitHub-App identity (separate two-pager).
- Not re-architecting `pr-review-fixer`'s triage contract.

## Business Risks and Mitigations

| Risk                                                   | Likelihood            | Mitigation                                                                                                                                                                            |
| ------------------------------------------------------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Naive fan-out regresses review quality (SWR-Bench)     | High if uncoordinated | Coordinator is mandatory; post-cutover monitoring + a documented rollback trigger restores the monolith if metrics regress                                                            |
| Cost balloons N× per cycle                             | Medium                | Risk-tier fan-out scales agents to diff size (D12) + shared-context (D13: no generated-file exclusion) + `sonnet` specialists / opus coordinator (D5 decided); then budget/monitoring |
| Instruction docs drift out of date                     | Medium                | Dedicated `pr-review-instruction-maker` specialist (D14) — flags framework/CI changes not reflected in `AGENTS.md`/`.claude/`                                                         |
| More agents raise raw false-positive volume            | Medium                | Coordinator reasonableness-filter + tool-verify; confidence ≥ 80 bar inherited by every specialist                                                                                    |
| Boundary grey-zones cause duplicate/mis-filed findings | Medium                | Written tie-breaker rule + coordinator owns re-categorization (esp. architecture↔correctness)                                                                                         |
| Governance drift across the two mirror harnesses       | Low                   | `npm run generate:bindings` + sync-validation gate on every phase touching an agent file                                                                                              |

The cross-cutting factual claims behind these risks live here; the corresponding **testable
scenarios** live in [prd.md §Acceptance Criteria](./prd.md#acceptance-criteria).
