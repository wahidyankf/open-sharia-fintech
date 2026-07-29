---
title: "Knowledge Capture Convention"
description: Standards for capturing generalizable learnings during plan execution in a transient learnings.md log, triaging each through an open-ended principle-based routing matrix, and enforcing two safety gates before any learning reaches a durable home
category: explanation
subcategory: development
tags:
  - knowledge-capture
  - learnings
  - plans
  - triage
  - safety-gates
  - post-mortems
created: 2026-07-05
---

# Knowledge Capture Convention

Every plan execution surfaces knowledge that outlives the plan itself — a rule worth codifying, a
fact worth documenting, an agent that should check for this next time, a bug that needs a test. Left
uncaptured, that knowledge evaporates when the plan folder moves to `done/`. Left uncaptured
_and unrouted_, it either vanishes silently or clutters a transient file nobody ever revisits. This
convention defines the transient `learnings.md` running log, the open-ended triage matrix that routes
each learning to the durable home that owns that kind of knowledge, the two hard safety gates every
entry must pass before routing, and the guardrails that keep the practice honest rather than
theatrical.

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: A learning that
  is noticed but never routed to a durable home is a symptom recurring in waiting. Routing a learning
  to the surface that owns its kind of knowledge (a convention, an agent, a test, a skill) is what
  actually prevents recurrence — not the act of writing it down.
- **[Documentation First](../../principles/content/documentation-first.md)**: Knowledge Capture
  treats the learnings a plan produces as a first-class deliverable of the plan, not an informal
  byproduct that lives only in the executor's working memory.
- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: The
  routing matrix is deliberately a single pass over a running log, not a dashboard, a database, or a
  standing review board. The anti-theater guardrails exist specifically to keep the mechanism this
  simple.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: The
  mandatory + explicit "none" escape means an empty `learnings.md` is never ambiguous — either it
  carries a routed/discarded record for every learning, or it carries an explicit
  `No generalizable learnings — <reason>` statement. Silence is never an accepted state.
- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: The litmus
  test ("would the system catch this next time?") forces a deliberate judgment before a learning is
  kept, rather than reflexively logging everything an executor happened to notice.

## Conventions Implemented/Respected

This convention implements/respects the following conventions:

- **[Plans Organization Convention](../../conventions/structure/plans.md)**: `learnings.md` is a plan
  folder artifact that follows the same lifecycle as the rest of the plan (backlog is not
  applicable; it accrues in `in-progress/` and moves with the plan on archival to `done/`).
- **[Feature Change Completeness Convention](./feature-change-completeness.md)**: When a learning
  routes to code (`apps/`, `libs/`, tests), the resulting follow-up plan is bound by this convention's
  specs/Gherkin two-path rule in full — Knowledge Capture does not create a side channel that bypasses
  it.
- **[Regression Test Mandate](./regression-test-mandate.md)**: When a learning identifies a bug, its
  code-routed follow-up plan carries the regression-test mandate exactly as any other bug fix would.
- **[Post-Mortem Convention](../../conventions/structure/post-mortems.md)**: Failure/incident learnings
  route through this convention's matrix to a post-mortem; that convention remains the single source
  of truth for post-mortem structure and content.
- **[No Secrets in Git Convention](../../conventions/security/no-secrets-in-committed-files.md)**: The
  secret/sensitivity safety gate below inherits this hard iron rule in full — `learnings.md` is
  committed and, in the public repos, world-readable.

## The Rule

**Every substantive plan MUST accrue a transient `learnings.md` running log during execution and
MUST triage every surviving entry through this convention's open-ended routing matrix, applying both
safety gates, before the plan is archived to `plans/done/`.** Archival is blocked until every entry
reaches a terminal state: routed inline, filed as a `plans/backlog/` follow-up, or discarded with a
one-line reason. A plan MAY record the explicit `No generalizable learnings — <reason>` escape
instead of individual entries, but it may never leave `learnings.md` silently empty.

## The Transient `learnings.md` Running Log

`learnings.md` is a plan-folder file, sibling to `delivery.md`, `prd.md`, and `tech-docs.md`:

```
plans/
├── in-progress/
│   └── my-plan/
│       ├── README.md
│       ├── brd.md
│       ├── prd.md
│       ├── tech-docs.md
│       ├── delivery.md
│       └── learnings.md          ← running log, accrued during execution
└── done/
    └── 2026-07-05__my-plan/
        ├── delivery.md
        └── learnings.md          ← moves with the plan; MAY be deleted later
```

**When it is written**: while executing delivery steps (the plan-execution workflow's execution
loop), not reconstructed from memory at the end. The moment an executor notices something
generalizable — a rule that should have been enforced, a fact that surprised them, a bug pattern, a
gap in a skill's instructions — they append a sanitized entry to `learnings.md` and keep working.
This is cheap in-the-moment capture, not a separate research task.

**Entry shape** (minimal, not a formal template):

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — see the secret/sensitivity gate)
- **Why it might generalize**: the litmus reasoning
```

**What it is NOT**: `learnings.md` is not a decision log, not a design-rationale document (that is
`tech-docs.md`'s job), and not a status report. It exists solely to stage candidate learnings for the
triage pass described below.

## The Triage Rubric: Open-Ended, Principle-Based Routing

The rubric is deliberately **open-ended** — it names common destinations but does not exhaust the
space. Route each learning to whichever durable home **owns that kind of knowledge**. Each learning
resolves to **exactly one** home, or is discarded.

### Candidate Durable Homes (including but not limited to)

| Home                                           | Route a learning here when...                                                                                                                                                                                                                                                                                            |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `repo-governance/` (rules / conventions / dev) | It is a **rule or standard** — something that should be required, forbidden, or standardized going forward.                                                                                                                                                                                                              |
| `docs/` (Diátaxis)                             | It is a durable **fact, how-to, tutorial, or explanation** a future reader would search for.                                                                                                                                                                                                                             |
| `.claude/agents/`                              | It changes **what a specific agent checks, makes, or fixes** — its instructions or behavior.                                                                                                                                                                                                                             |
| `.claude/skills/`                              | It is **procedural know-how** an agent should load on-demand to perform a task well.                                                                                                                                                                                                                                     |
| `apps/` and `libs/` **source code**            | It is an actual **bug fix, refactor, or new feature** — codebase behavior itself must change.                                                                                                                                                                                                                            |
| **tests**                                      | It needs a **new regression test or added coverage** so the failure cannot recur unnoticed.                                                                                                                                                                                                                              |
| `docs/explanation/post-mortems/`               | It is a **failure/incident** learning — route to a post-mortem (cross-reference; do not duplicate content). See the [Post-Mortem Convention](../../conventions/structure/post-mortems.md).                                                                                                                               |
| `plans/ideas/` (a two-pager idea brief)        | It is a **future-work idea** — richer than a one-liner, not yet plan-ready — that needs its own pitch/triage before it can become a full plan. Fold it into an existing two-pager if one already covers the same area (see the [Ideas Folder convention](../../conventions/structure/plans.md#ideas-folder-two-pagers)). |
| `discard — not generalizable`                  | It fails the litmus: the system would **not** catch this automatically next time even if routed. Log a one-line reason.                                                                                                                                                                                                  |

This list is not exhaustive. A learning may route to any durable surface that owns its kind of
knowledge — these are simply the homes that recur most often in this repository.

### The Litmus Test (capture vs. discard)

**Keep a learning only if, once routed, the system would catch this automatically next time.** If
nothing durable would change behavior as a result of routing it, discard the learning with a one-line
reason. This is the deliberate guard against over-capture: a learning that cannot possibly change
future behavior through any durable surface is noise, not knowledge.

Apply the litmus to every candidate entry before doing anything else with it — before sanitizing,
before picking a home. An entry that fails the litmus is discarded immediately; the safety gates below
apply only to entries that survive it.

## The Code-Routing Downstream Rule

When a learning's home is `apps/`, `libs/`, or tests — i.e., the codebase itself must change — that
follow-up work is **always** a separate `plans/backlog/` plan. It is **never landed inline** in the
current plan's commits or PR.

**Why**: a code change is bound by the repository's normal engineering gates, and a captured learning
does not get to bypass them:

- **[Feature Change Completeness](./feature-change-completeness.md)**: an observable behavior change
  in `apps/`/`libs/` ships with companion `specs/` Gherkin, carried by the follow-up plan.
- **[Regression Test Mandate](./regression-test-mandate.md)**: if the learning names a bug, its fix
  lands with a reproducing test (failing before, passing after) in the same commit/PR as the fix.
- **[Test-Driven Development](../workflow/test-driven-development.md)**: Red → Green → Refactor
  governs the code change itself.

Because these gates apply, a code-routed learning is filed as its own `plans/backlog/<slug>/`
plan (which then carries its own specs/Gherkin, regression-test, and TDD obligations when executed) —
never smuggled into the current governance/docs plan's PR.

**Carve-out (Iron Rule 3 — Root Cause Orientation still applies in full)**: this downstream rule
governs learnings captured for **future** evolution. A bug, failing test, or lint failure the
executor must fix to finish the **current** plan's own deliverables is a **blocker** — ordinary
inline execution under Root Cause Orientation ("fix all issues, including preexisting"), not a
deferred learning. The "always a separate backlog plan" rule applies only to code changes a learning
_suggests_ as a future improvement that are **not required** to complete the current plan. Do not
misuse this carve-out to smuggle unrelated code changes into a docs/governance plan — it covers
only what is genuinely required to finish the plan's own scope.

## Routing Timing: Destination-Aware (Inline vs. Backlog)

Timing has a hard boundary determined by **destination**, not by convenience:

- **Non-code homes** (`docs/`, `repo-governance/`, `.claude/agents/`, `.claude/skills/`,
  `post-mortems/`, and any other non-code home): a **small** edit MAY land **inline** in the current
  plan's own commit/PR. A learning implying **large new work** becomes a tracked
  `plans/backlog/<slug>/` follow-up plan instead. The `learnings.md` entry records which
  path was taken (and the backlog path, if filed).
- **`plans/ideas/` two-pager** (a non-code home): a **future-work idea that is not yet plan-ready**
  becomes a two-pager filed **inline** in the current plan's own commit/PR (creating one
  `plans/ideas/<slug>.md` is a small doc edit). Distinguish from `backlog/`: a learning that is
  **already plan-ready** goes straight to a `plans/backlog/<slug>/` follow-up plan; a
  promising-but-unripe idea that still needs its own pitch/triage goes to `plans/ideas/`. Fold into an
  existing two-pager rather than duplicating. This routes the **pre-plan brief only** — any eventual
  code work still flows through a full backlog plan when the two-pager is promoted, carrying the
  code-routing gates above in full.
- **Code homes** (`apps/`, `libs/`, tests): per the code-routing downstream rule above, **always** a
  separate `plans/backlog/` plan — **never** inline, no exceptions besides the Iron Rule 3
  current-plan-blocker carve-out.
- **Discard**: logged with a one-line reason; no further action.

Archival is **BLOCKED** until every `learnings.md` entry reaches one of three terminal states:

1. **Routed inline** (non-code homes only) — the edit has landed in this plan's own commits.
2. **Filed** as a `plans/backlog/` plan (any home; **mandatory** for code) — the entry records the
   backlog folder path.
3. **Discarded** with a one-line reason.

Nothing is silently dropped, and nothing sits in an open, undecided state at archival time.

## The Two Safety Gates (HARD — run before routing)

Both gates are mandatory triage steps for every surviving entry, applied **before** any routing
decision is finalized. They are the repository's belt-and-suspenders: prose gates for the executor
performing the triage, and explicit verification checks for the completion checker that gates
archival.

### 1. Secret/Sensitivity Gate

`learnings.md` is committed to git and, in the public repos, world-readable. A learning MUST NEVER
contain a secret, credential, token, API key, private IP/hostname, or insecure implementation detail.

- Sanitize by replacing the sensitive value with a `<placeholder>` token and stating where the real
  value lives — this inherits the [No Secrets in Git](../../conventions/security/no-secrets-in-committed-files.md)
  hard iron rule and the post-mortem placeholder pattern (`<api-token>`, `<db-connection-url>`, and
  so on).
- **If a learning cannot be sanitized without losing its meaning, discard it.** A learning whose only
  content is a secret is not generalizable knowledge; it is a liability.
- This gate runs on every surviving entry regardless of destination — even a learning destined for a
  private repo must not carry a raw secret into a committed file.

### 2. Repo-Relevance Gate

A learning routes **only** to the repo(s) it actually pertains to:

- **Infra-private content** (Terraform, k3s, Proxmox, `coralpolyp`, on-prem infrastructure, real
  hostnames or inventories) MUST stay in `ose-private` **only** and MUST NEVER cross-route into the
  public `ose-public` / `ose-primer` repos.
- **Public-governance content** MAY propagate `ose-public` → `ose-primer` via the existing parity
  loop (see the
  [Multi-Repo Parity Planning workflow](../../workflows/plan/plan-multi-repo-parity-planning.md)).
- An **infra-specific** learning never appears in any file destined for a public repo, even in
  sanitized form — the gate is about which repo the knowledge belongs in, not just whether it is
  safe to publish.

Both gates run before a home is chosen and before any timing decision is made. A learning that fails
either gate is discarded (secret gate) or scoped down to a single private repo (repo-relevance gate) —
it never proceeds to routing in a form that violates either constraint.

## Mandatory + Explicit "None" Escape

The Knowledge Capture phase is **mandatory** for substantive plans — it MUST be present and it MUST
run. But requiring a phase does not mean fabricating learnings that were never observed.

**Never leave `learnings.md` silently empty.** If a plan's execution genuinely surfaced no
generalizable learning, record the explicit escape:

```markdown
No generalizable learnings — <one-line reason>
```

For example: `No generalizable learnings — pure mechanical rename, no new patterns surfaced.`

This explicit record is a **pass**, not a finding. A checker never penalizes an honest "none". What
a checker DOES penalize is **silence**: a plan with no `learnings.md` content at all, and no
explanation for its absence, at MEDIUM criticality (see
[Criticality Levels Convention](./criticality-levels.md)).

## Exemptions

Pure-docs and trivial plans MAY skip elaborate Knowledge Capture — this mirrors the existing
exemption pattern in [Feature Change Completeness](./feature-change-completeness.md#two-paths-with-a-plan-and-without-a-plan)
for the specs/Gherkin two-path rule. A one-line rename, a single broken link fix, or an equivalently
trivial plan does not require a populated `learnings.md`; the explicit "none" escape above (or an
equally explicit note in `delivery.md`) satisfies the requirement without inventing insight from a
change that had none to offer.

## Anti-Theater Guardrails

A knowledge-capture practice can fail in two opposite directions, and this convention guards against
both:

- **Under-capture** (nothing is ever recorded): the mandatory phase + the explicit "none" escape +
  the MEDIUM-severity checker finding on silent absence together make skipping the practice visible
  and flagged, not silently tolerated.
- **Over-capture** (everything is logged and nothing is ever triaged): the litmus test discards
  non-generalizable noise up front; archival being blocked on triage completion means an untriaged
  backlog of entries cannot simply accumulate forever inside a live plan.

Beyond that balance, the mechanism itself must avoid becoming theater:

- **Single named owner**: the plan executor who accrues `learnings.md` is also the one who runs the
  triage pass at the end of the same plan — no separate role, no hand-off, no committee.
- **Lives in a tool already opened**: `learnings.md` sits in the plan folder the executor already has
  open for `delivery.md`; this is deliberately NOT a new dashboard, ticketing system, or standalone
  tracker that requires a separate tool to maintain.
- **Fixed-cadence review**: the triage pass happens once, at a fixed point in the plan lifecycle (the
  final substantive phase, immediately before archival) — not on an ad-hoc or indefinitely deferred
  schedule.

## The Transient-Log Caveat

**`learnings.md` is transient scaffolding. It is NEVER the system of record.**

`plans/done/*/learnings.md` MAY be deleted at any future date — `plans/done/` is a historical
record of plan execution, not a permanent knowledge archive. Consequently:

- Everything worth keeping from a learning MUST be routed to a durable home (a convention, a doc, an
  agent, a skill, code, a test, or a post-mortem) **before** archival. Routing-out is mandatory
  pre-archival, not optional cleanup.
- **No process, agent, or future plan may depend on querying `learnings.md` later.** If something in
  a `learnings.md` entry matters, it must already live somewhere durable by the time the plan is
  archived. Treat `learnings.md` as safe to delete the moment its entries are all terminal.
- This caveat is why the routing matrix's timing rule (inline vs. backlog) and the mandatory-terminal
  rule at archival both exist: they are what actually makes `learnings.md`'s transience safe.

## What Gets Validated

Enforcement is by **agent checkers reading prose**, not a `rhino-cli` structural validator —
triaging generalizability is a judgment call a deterministic tool cannot make. The relevant agents
are:

- **`plan-checker`**: flags a substantive plan whose `delivery.md` has no Knowledge Capture phase and
  no explicit "none" record, at **MEDIUM** criticality. An explicit "none" record passes without a
  finding.
- **`plan-execution-checker`**: blocks archival until every `learnings.md` entry is routed-inline
  (non-code only), filed-as-a-backlog-plan (mandatory for code), or discarded-with-reason; verifies
  both safety gates were applied; verifies no code born from a learning landed inline.
- **`plan-fixer`**: scaffolds a missing Knowledge Capture phase and `learnings.md` file into a plan
  that lacks them.
- **`plan-maker`** and the plan-creating skill: emit the Knowledge Capture phase and the
  `learnings.md` scaffold into every new substantive plan by default.

## Examples

### PASS: Learning routed inline (non-code, small)

```markdown
## Learning: worktree-setup doc omitted a step

- **Context**: Provisioning the worktree for this plan required an undocumented
  `npm run doctor -- --fix` re-run after a stale toolchain cache.
- **Observation**: `repo-governance/development/workflow/worktree-setup.md` did not mention this
  re-run step.
- **Why it might generalize**: the next plan author will hit the same stale-cache surprise.

**Routing**: `repo-governance/development/workflow/worktree-setup.md` (non-code, small) — routed
INLINE, landed in commit `abc1234` of this plan.
```

### PASS: Learning filed as backlog (code, mandatory)

```markdown
## Learning: rhino-cli doctor command silently swallows a missing-tool exit code

- **Context**: Noticed while running `npm run doctor -- --fix` during Phase 0.
- **Observation**: a missing tool that fails to install still reports "0 warnings" in the summary
  line.
- **Why it might generalize**: a future contributor could believe their toolchain is healthy when
  it is not — the system would not catch this without a code fix.

**Routing**: `apps/rhino-cli` (code) — ALWAYS filed as backlog. Filed at
`plans/backlog/fix-doctor-silent-tool-failure/`. NOT landed inline in this plan's PR.
```

### PASS: Learning discarded (fails the litmus)

```markdown
## Learning: the executor personally found Nx's cache output confusing at first

- **Context**: Ran `nx affected` for the first time in this session.
- **Observation**: took a moment to parse the cache-hit summary.
- **Litmus**: no durable surface would change behavior by routing this — it is a one-time
  orientation moment, not a gap in documentation (the docs already explain cache output).

**Routing**: discard — not generalizable; existing docs already cover this, no gap found.
```

### PASS: Explicit "none" escape

```markdown
No generalizable learnings — this plan renamed one file and updated its three inbound links; no
new pattern, rule, or gap surfaced during execution.
```

### FAIL: Silent absence

```markdown
<!-- learnings.md does not exist; delivery.md has no Knowledge Capture phase; no explanation given -->
```

`plan-checker` flags this at MEDIUM: the phase is mandatory, and its absence carries no explicit
"none" record.

### FAIL: Code change landed inline instead of backlogged

```markdown
**Routing**: `apps/organiclever-be` (code) — routed INLINE, landed in commit `def5678` of this
governance plan's PR.
```

This is a **plan-execution-checker** blocking finding: a code-homed learning must be filed as a
separate `plans/backlog/` plan, never landed inline, regardless of how small the fix looks.

### FAIL: Secret leaked into learnings.md

```markdown
## Learning: the staging database connection string is postgres://admin:hunter2@10.0.4.12:5432/app
```

Fails the secret/sensitivity gate outright — discard, or rewrite as
`postgres://<user>:<placeholder>@<staging-db-host>:5432/<db-name>` if the underlying insight (e.g.,
"the staging connection string format differs from production") is itself worth keeping.

### FAIL: Infra-private content cross-routed to a public repo

```markdown
**Routing**: `repo-governance/` in `ose-public` — this k3s node's real hostname handling should be
documented here.
```

Fails the repo-relevance gate: infra-specific content (a real k3s node/hostname) must stay in
`ose-private` only, never in `ose-public` or `ose-primer`.

## Related Documentation

- [Plans Organization Convention](../../conventions/structure/plans.md) — plan folder structure and
  lifecycle; documents `learnings.md` and the Knowledge Capture phase as part of plan structure.
- [Post-Mortem Convention](../../conventions/structure/post-mortems.md) — authoritative structure
  for post-mortems; failure/incident learnings route here via this convention's matrix.
- [Feature Change Completeness Convention](./feature-change-completeness.md) — the specs/Gherkin
  two-path rule that binds every code-routed learning's follow-up plan.
- [Regression Test Mandate](./regression-test-mandate.md) — the bug-fix testing obligation that
  binds every code-routed learning that names a bug.
- [Criticality Levels Convention](./criticality-levels.md) — the CRITICAL/HIGH/MEDIUM/LOW scale used
  by `plan-checker`'s silent-absence finding.
- [No Secrets in Git Convention](../../conventions/security/no-secrets-in-committed-files.md) — the hard iron rule
  the secret/sensitivity gate inherits.
- [Plan Execution Workflow](../../workflows/plan/plan-execution.md) — Step 2 running-log capture and
  the Step 8 Knowledge Capture phase before archival.
- [plan-maker](../../../.claude/agents/plan-maker.md) — emits the Knowledge Capture phase and
  `learnings.md` scaffold into new plans.
- [plan-checker](../../../.claude/agents/plan-checker.md) — flags silent absence of the phase.
- [plan-execution-checker](../../../.claude/agents/plan-execution-checker.md) — blocks archival
  until routing and both safety gates are complete.
- [plan-fixer](../../../.claude/agents/plan-fixer.md) — scaffolds a missing phase.
