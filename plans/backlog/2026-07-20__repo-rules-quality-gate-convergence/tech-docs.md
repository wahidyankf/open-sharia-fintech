# Technical Documentation — Repo Rules Quality Gate Convergence

## Architecture

### Current loop (as built)

```mermaid
%% Current repo-rules-quality-gate loop — one search shape, one termination rule
flowchart LR
  A[rhino-cli preflight<br/>4 deterministic categories] --> B[repo-rules-checker<br/>AI semantic sweep]
  B --> C{threshold<br/>findings > 0?}
  C -- yes --> D[repo-rules-fixer<br/>instance-level fix]
  D --> A
  C -- no --> E{consecutive<br/>zeros >= 2?}
  E -- no --> B
  E -- yes --> F[pass]

  style A fill:#56B4E9,stroke:#04395E,color:#000000
  style B fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style D fill:#D55E00,stroke:#7A3600,color:#FFFFFF
  style F fill:#009E73,stroke:#006147,color:#FFFFFF
```

The preflight already covers four mechanical categories, but **none of them measures sweep
completeness**. The AI checker picks its own search shape each round, and nothing records or
constrains that shape — so a zero means "this round's search found nothing", not "the text is
consistent".

### Target loop (this plan)

```mermaid
%% Target loop — sweep-completeness gate, transcript, and an adversarial round before pass
flowchart LR
  P[rhino-cli preflight<br/>+ sweep-completeness] --> Q{never-touched<br/>candidates > 0?}
  Q -- yes --> R[repo-rules-fixer<br/>class-wide sweep<br/>+ self-drift recheck]
  R --> P
  Q -- no --> S[repo-rules-checker<br/>inbound-link sweep<br/>+ transcript]
  S --> T{in-scope<br/>findings > 0?}
  T -- yes --> R
  T -- no --> U[adversarial round<br/>agenda = never-touched set]
  U --> V{adversarial<br/>zero?}
  V -- no --> R
  V -- yes --> W[pass]

  style P fill:#56B4E9,stroke:#04395E,color:#000000
  style S fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style R fill:#D55E00,stroke:#7A3600,color:#FFFFFF
  style U fill:#CC79A7,stroke:#6B2F55,color:#000000
  style W fill:#009E73,stroke:#006147,color:#FFFFFF
```

### Sweep-set derivation

```mermaid
%% How the sweep set is built — stable keys first, phrasing second
flowchart TD
  G[changed governing document] --> H[inbound links:<br/>documents linking TO it]
  G --> I[outbound links:<br/>documents it links to]
  G --> J[declared blast radius:<br/>agents + workflows + skills<br/>naming the rule]
  H --> K[candidate set]
  I --> K
  J --> K
  K --> L[secondary lens:<br/>keyword phrasing search<br/>WITHIN the candidate set]
  K --> M[never-touched set =<br/>candidates minus<br/>corrective-commit union]

  style K fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style M fill:#CC79A7,stroke:#6B2F55,color:#000000
```

The critical inversion: today keyword search **selects** the files, so any file whose wording differs
is invisible. In the target design, links and declared blast radius select the files, and keyword
search only ranks within that set.

### Lens sequencing across a round

```mermaid
%% Order of operations within one gate execution
sequenceDiagram
  participant O as Orchestrator
  participant D as rhino-cli (deterministic)
  participant C as repo-rules-checker
  participant F as repo-rules-fixer
  participant R as Blind-Spot Registry

  O->>D: repo-governance audit (incl. sweep-completeness)
  D->>D: compute candidate set and never-touched set
  D-->>O: mechanical findings (zero-token)
  alt never-touched candidates exist
    O->>F: class-wide sweep over the untouched candidates
    F->>F: re-check own change surface for self-inflicted drift
    F-->>O: fix report + sweep transcript
  else clean
    O->>C: semantic sweep over the candidate set
    C->>R: consult blind-spot classes
    C-->>O: findings + verbatim sweep transcript
  end
```

### Finding-evidence decision branch

```mermaid
%% How a claim becomes accepted evidence — the false-alarm path is explicit
flowchart TD
  E[claim under validation] --> G{claim about<br/>mechanical behavior?}
  G -- no --> N[normal semantic review]
  G -- yes --> H{verified against the<br/>implementing file?}
  H -- no --> X[reject as unverified<br/>doc-restating-doc]
  H -- yes --> I{evidence from a<br/>validator invocation?}
  I -- no --> OK[accept]
  I -- yes --> J{invocation matches<br/>CI flags?}
  J -- no --> K{divergence<br/>justified in report?}
  K -- no --> X
  K -- yes --> OK
  J -- yes --> OK

  style X fill:#D55E00,stroke:#7A3600,color:#FFFFFF
  style OK fill:#009E73,stroke:#006147,color:#FFFFFF
```

### Blind-spot lifecycle

```mermaid
%% A single stale passage's states from introduction to closure
stateDiagram-v2
  [*] --> Stale: governing rule changed elsewhere
  Stale --> InCandidateSet: selected by inbound link or blast radius
  Stale --> Invisible: missed by keyword-shaped search
  Invisible --> InCandidateSet: stable-key sweep adopted
  InCandidateSet --> ClassSwept: fixer sweeps whole class
  ClassSwept --> ClosureVerified: adversarial round finds no residue
  ClosureVerified --> [*]: closed
  ClosureVerified --> Stale: fixer's own commit falsified another claim
```

The `ClosureVerified --> Stale` edge is blind-spot class 11 — the self-inflicted drift loop that
commit `362c23aab` had to close.

### Tri-repo propagation dependency

```mermaid
%% Propagation order — ose-public is the source of truth
flowchart LR
  A[ose-public<br/>Phases 1-6] --> B[ose-primer<br/>Phase 7]
  A --> C[ose-infra<br/>Phase 8]
  B -.byte-identity check.-> A
  C -.byte-identity check.-> A

  style A fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style B fill:#56B4E9,stroke:#04395E,color:#000000
  style C fill:#56B4E9,stroke:#04395E,color:#000000
```

### Delivery phase flow

```mermaid
%% Phase progression with gates
flowchart LR
  P0[Phase 0<br/>baseline] --> P1[Phase 1<br/>registry]
  P1 --> P2[Phase 2<br/>validator]
  P1 --> P3[Phase 3<br/>sweep contracts]
  P2 --> P4[Phase 4<br/>evidence grounding]
  P3 --> P4
  P4 --> P5[Phase 5<br/>adversarial termination]
  P5 --> P6[Phase 6<br/>replay + bindings + PR]
  P6 --> P7[Phase 7<br/>ose-primer]
  P6 --> P8[Phase 8<br/>ose-infra]
  P7 --> P9[Phase 9<br/>knowledge capture]
  P8 --> P9

  style P0 fill:#009E73,stroke:#006147,color:#FFFFFF
  style P6 fill:#0072B2,stroke:#04395E,color:#FFFFFF
  style P9 fill:#CC79A7,stroke:#6B2F55,color:#000000
```

Phases 2 and 3 are independent of each other and may run in parallel (subject to the repo's
concurrency cap); Phases 7 and 8 likewise.

## Blind-Spot Class Registry — seed content

The registry lands at `repo-governance/development/quality/governance-sweep-blind-spots.md`
[Repo-grounded — verified absent via `test -f` on `main` during authoring].

**Evidence durability (DECISION 8)**: each entry embeds its evidence inline — the commit subject and
the file list proving the miss — because the cited SHAs live on the unmerged branch
`parallel-orchestration-shared-machine-governance` and will not survive a squash-merge. The SHA is a
best-effort pointer, never the sole evidence.

### The twelve seed classes

| ID    | Blind spot                          | Missing sweep form                                    | Catching sweep form                                             | Evidence (commit subject)                                        |
| ----- | ----------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------- |
| BS-1  | Fixed term order                    | Ordered multi-term pattern                            | Order-independent alternation; inspect table cells separately   | `sweep stale direct-push-default boilerplate to all four copies` |
| BS-2  | Generative-source-only scope        | Edit the doc that generated the rule                  | Include convention + checker + fixer + maker siblings           | `sweep stale direct-push-default boilerplate to all four copies` |
| BS-3  | Bracketed-tag / plural assumption   | Search the tagged form `[HUMAN]` only                 | Search the untagged prose form too (`human merge`)              | `close the unbracketed "human merge" sweep gap`                  |
| BS-4  | Paraphrase                          | Any keyword-selected search                           | Inbound-link sweep — select by link, not by wording             | `sweep by inbound link, catching the paraphrase survivors`       |
| BS-5  | Teaching vs normative content       | Sweep only normative sections                         | Include explanatory/teaching prose in the candidate set         | `rewrite the teaching content that still taught main-by-default` |
| BS-6  | Untouched sections in touched files | Treat a file as done once edited                      | Re-scan the whole file, not the edited region                   | `rewrite the untouched teaching sections in partly-fixed files`  |
| BS-7  | Worked examples contradicting prose | Sweep prose only                                      | Diff each example against the paragraph governing it            | `align worked examples with the prose above them`                |
| BS-8  | Agent-emitted templates             | Sweep documentation only                              | Include templates agents emit into other artifacts              | `make post-push CI templates delivery-mode-aware`                |
| BS-9  | Obligation scoped to old condition  | Search the changed value                              | Search the **condition** the obligation is keyed on             | `scope CI post-push verification to the delivery target`         |
| BS-10 | Definition blocks                   | Sweep usage sites                                     | Include the definition/glossary blocks defining the term        | `correct the TBD definition block and the main-ci gate doc`      |
| BS-11 | Self-inflicted drift                | Sweep only pre-existing content                       | Re-check the chain's own change surface for claims it falsified | `correct nx-targets CI-trigger claims for main-ci schedule`      |
| BS-12 | Directory-scoped sweep              | `grep -r … repo-governance/` while claiming repo-wide | Repo-wide, or enumerate + justify every exclusion               | `correct main-ci trigger docs outside repo-governance`           |

### BS-12 — worked entry (the highest-cost class)

**Symptom**: a sweep restricted to one subtree, reported as repo-wide. Eleven consecutive rounds
asserted repo-wide scope without demonstrating it.

**Inline evidence** (survives SHA loss): the final corrective commit
`correct main-ci trigger docs outside repo-governance` was the **first** in a twelve-commit chain to
touch any of:

```text
.github/workflows/README.md
specs/apps/ayokoding/containers/container.md
specs/apps/organiclever/containers/container.md
```

`docs/` was first reached only at the eighth commit (`scope CI post-push verification to the delivery
target` / `correct the TBD definition block…`). The union of all twelve commits touches 46 files
[Repo-grounded — `git diff --name-only 488148eca..c30ac344e | wc -l` returns 46].

**Missing form**: a recursive search rooted at `repo-governance/`.

**Catching form**: repo-wide search, or a search whose exclusions are enumerated as literal globs and
justified in the report.

**Detection**: statically detectable — a recorded sweep command whose root is a subdirectory, or
whose exclusion set is non-empty and unjustified.

### BS-4 — worked entry (the controlled comparison)

**Symptom**: stale text containing none of the search keywords. The observed instance read
"Explicit user approval required" — no occurrence of the changed tag, the changed default, or any
term a reasonable keyword sweep would have chosen.

**Inline evidence**: commit `sweep by inbound link, catching the paraphrase survivors` — the first
round to select files by inbound link rather than by phrasing, and it found survivors that four
prior keyword-shaped rounds had missed. This is the single controlled comparison in the chain and is
the basis of DECISION 2.

**Missing form**: any search that selects candidate files by matching their text.

**Catching form**: enumerate documents linking to the changed governing document; sweep all of them
regardless of wording.

**Detection**: partially static — the validator can verify the inbound-link set was enumerated;
whether a given passage is stale stays an AI judgement.

## Design Decisions

### DD-1 — the registry is a governance quality document, not agent-inlined prose

Inlining twelve class descriptions with evidence into `repo-rules-checker.md`, `repo-rules-fixer.md`
and `repo-rules-maker.md` would triple their content and push against the instruction-file size
budget [Repo-grounded — `nx run rhino-cli:instruction-size:validation` exists and is wired into the
preflight as the `instruction-size` category]. One governance file that all three link to keeps a
single source of truth and one place to append class thirteen.

### DD-2 — the deterministic pass is a fifth `repo-governance audit` category

The orchestrator today runs exactly four categories — `layer-coherence`, `traceability-audit`,
`vendor-audit`, `instruction-size` [Repo-grounded — `repo-rules-quality-gate.md` Step 0.5]. Adding
`sweep-completeness` as a fifth means the checker consumes it through the Step 0.5 JSON envelope it
already parses, with no new plumbing and no new invocation for an agent to skip.

Cost: `apps/rhino-cli` must stay byte-identical across all three repos per the
[SDLC Gate Standard](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary),
so this adds a Gherkin behavior tree under `specs/apps/rhino/behavior/rhino-cli/gherkin/` and
tri-repo propagation weight. This is the plan's largest reversible commitment (DECISION 1); Phase 2
is authored to be separable — dropping it degrades the plan to mechanisms 1 and 3-6 without
restructuring any other phase.

### DD-3 — the candidate set is bounded by links and declared blast radius

A naive never-touched set would be "every file in the repo", which is useless. The candidate set is:

1. every document with an **inbound link** to the changed governing document;
2. every document the changed document **links out** to;
3. the **declared blast radius** — agents, workflows and skills naming the changed rule.

The never-touched set is the candidate set minus the union of the chain's corrective commits. This
keeps the adversarial round's agenda finite and relevant, which is what stops it degenerating into
free-form doubt (a named product risk).

### DD-4 — sweep transcript over sweep assertion

The workflow cannot verify a sweep it cannot see. Recording the verbatim command plus the exclusion
set converts an unfalsifiable claim into a checkable one, and costs one line in a report. This is the
cheapest mechanism in the plan and closes BS-12 even without the validator.

### DD-5 — evidence grounding has two rules, not one

Rule A: a claim about mechanical behavior is verified against the **implementing** file (workflow,
hook, script), never against another document restating it. Closes BS-11.

Rule B: a validator invocation cited as evidence must match **CI's exact flags**, or record a written
justification for diverging. Closes the observed false alarm, where a bare `md mermaid validate`
flagged the validator's own negative fixtures. CI invokes it with
`--exclude apps/rhino-cli/tests/fixtures --exclude plans/done`, while the `package.json` lint-staged
entry uses the bare form [Repo-grounded — both verified on `main` during authoring]. The two rules
ship together because both failures are "trusted the wrong artifact as evidence".

### DD-6 — termination is adversarial, not merely repeated

Two consecutive zeros from the same search shape is one observation repeated, not two observations.
The adversarial round changes the shape: its agenda is the mechanically derived never-touched set,
so it interrogates exactly the region the semantic rounds structurally could not see. An empty
agenda is reported explicitly (AC-13) so that "nothing to challenge" is distinguishable from "the
computation never ran".

### DD-7 — the falsified convergence claim is corrected, not deleted

`maker-checker-fixer.md` §Preventing Iteration Loops claims convergence in 1-3 iterations with
escalation after 5 [Repo-grounded — both phrases verified present on `main`]. The archived chain ran 13. The text is rewritten to describe the phased budget and cite the falsifying chain, rather than
silently dropped, so the next reader understands why the number changed and does not restore it.

### DD-8 — evidence is embedded inline because the SHAs are perishable

See README DECISION 8. The evidence commits are branch-local and this repo squash-merges, so SHA
citations die on merge. Each registry entry carries its commit subject and proving file list inline.
Delivery steps that replay the chain resolve SHAs **defensively** — if `git cat-file -t <sha>` fails,
the step falls back to the inline evidence rather than failing the phase.

## UI-Design-Funnel Exemption

This plan is **not UI-bearing**. It changes governance markdown, agent definitions, and a CLI
validator that emits text to stdout. It adds and changes no user-facing screen or component under
`apps/` or `libs/` that renders to an end user. Per the
[UI Mockups in Plan Docs convention](../../../repo-governance/conventions/formatting/diagrams.md#ui-mockups-in-plan-docs),
the design funnel does not apply, and this paragraph is the explicit exemption record.

## Testing Strategy

| Mechanism                  | Test level                | How the Gherkin binds                                                                 |
| -------------------------- | ------------------------- | ------------------------------------------------------------------------------------- |
| Registry entries           | Inline-evidence review    | AC-1, AC-2 — each entry's proving file list is checked against the inline evidence    |
| Never-touched computation  | Rust unit + Gherkin specs | AC-3 — RED tests against fixture repo states with known candidate and touched sets    |
| Directory-scope detection  | Rust unit + Gherkin specs | AC-4 — RED tests against sweep-report fixtures with and without enumerated exclusions |
| Agent contract text        | Grep-based gate checks    | AC-5 through AC-11 — presence and shape verified mechanically, semantics by review    |
| Adversarial termination    | Workflow text + review    | AC-12, AC-13 — termination criteria read and verified                                 |
| Convergence-claim removal  | Grep both directions      | AC-14 — phrase present pre-edit (returns 1), absent post-edit (returns 0)             |
| No-check-removed invariant | Inventory diff            | AC-15 — Phase 0 records the baseline inventory; Phase 6 compares                      |
| Bindings + byte identity   | Existing repo validators  | AC-16, AC-17 — `npm run generate:bindings`, harness sync validation, byte-identity    |

Per [Test-Driven Development](../../../repo-governance/development/workflow/test-driven-development.md),
the validator's tests are written before its implementation; each RED step in
[delivery.md](./delivery.md) carries exactly one bound scenario.

## Surface Inventory

| #   | Surface                                                                  | Change                                                          | Grounding                    |
| --- | ------------------------------------------------------------------------ | --------------------------------------------------------------- | ---------------------------- |
| 1   | `repo-governance/development/quality/governance-sweep-blind-spots.md`    | **Create** — the BSCR                                           | [Repo-grounded] absent today |
| 2   | `repo-governance/workflows/repo/repo-rules-quality-gate.md`              | Step model, termination criteria, adversarial round             | [Repo-grounded] exists       |
| 3   | `repo-governance/development/pattern/maker-checker-fixer.md`             | Corrected convergence guidance; sweep methodology               | [Repo-grounded] exists       |
| 4   | `.claude/agents/repo-rules-checker.md`                                   | Inbound-link sweep, transcript, evidence grounding, adversarial | [Repo-grounded] exists       |
| 5   | `.claude/agents/repo-rules-fixer.md`                                     | Class-wide sweep, self-drift recheck, transcript                | [Repo-grounded] exists       |
| 6   | `.claude/agents/repo-rules-maker.md`                                     | BSCR link; start propagation from the inbound-link set          | [Repo-grounded] exists       |
| 7   | `apps/rhino-cli/src/commands/governance_sweep_completeness.rs`           | **Create** — the validator                                      | [Repo-grounded] dir exists   |
| 8   | `apps/rhino-cli/src/cli.rs`, `commands.rs`, `governance_audit.rs`        | Register the fifth audit category                               | [Repo-grounded] all exist    |
| 9   | `specs/apps/rhino/behavior/rhino-cli/gherkin/repo-governance/`           | **Create** — `repo-governance-sweep-completeness.feature`       | [Repo-grounded] dir exists   |
| 10  | `repo-governance/development/quality/README.md`, `development/README.md` | Register the new convention in the index tables                 | [Repo-grounded] exist        |
| 11  | `.opencode/`, `.amazonq/`                                                | **Regenerated only** — never hand-edited                        | Generated artifacts          |
| 12  | `ose-primer`, `ose-infra`                                                | Propagation of surfaces 1-10                                    | Sibling repos                |

## Dependencies

- `npm run generate:bindings` — regenerates `.opencode/` and `.amazonq/` from `.claude/`
- `npx nx affected -t typecheck lint test:quick specs:coverage` — the standing quality gate
- `cargo` via the existing rhino-cli Nx targets — validator build and test
- `git` plumbing (`git log`, `git diff --name-only`, `git cat-file`) — never-touched computation
- `gh` CLI — PR creation and the review cycle

## Rollback

Every surface is additive or text-level. Rollback is `git revert` of the phase PR. The validator is
introduced advisory-first — it reports findings into the existing preflight envelope, which the
workflow's Step 2 already treats as visibility-only and never counts toward the mode threshold
[Repo-grounded — `repo-rules-quality-gate.md` Step 2]. A defective validator therefore degrades to
noise rather than to a blocked gate. The registry is inert data. No migration, no persisted state, no
schema change.
